#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
#include <string>
using namespace std;

struct Node
{
	int pre;
	char input;
	int next;

	Node(int pre,char input,int next)
	{
		this->pre = pre;
		this->input = input;
		this->next = next;
	}
};

struct Dtran
{
	vector<int> pre;
	char input;
	vector<int> next;

	Dtran(vector<int> pre, char input, vector<int> next)
	{
		this->pre = pre;
		this->input = input;
		this->next = next;
	}
};

class MyClass
{
private:
	string reStr;
	int status;
	vector<Node*> trans;
	vector<Dtran*> DFA;
	vector<int> finish;

public:
	MyClass()
	{
		reStr = "";
		status = 0;
	}

	MyClass(string str)
	{
		reStr = str;
		status = 0;
	}

	void reToNFA();
	void printNFA();
	vector<int> closure(int s);
	vector<int> closure(vector<int> s);
	vector<int> move(vector<int> T, char a);
	void NFAToDFA();
	void printDFA();
	void accept(char a[]);
};

void MyClass::reToNFA()
{
	stack<int> start;
	stack<char> reChar;
	stack<int> end;

	reChar.push('$');
	start.push(status++);
	end.push(status++);

	for (auto i = reStr.begin(); i != reStr.end(); i++)
	{
		char ch = *i;
		switch (ch)
		{
		case '(':
		{
			start.push(status++);
			end.push(status++);
			int next = start.top();
			start.pop();
			int pre = start.top();
			trans.push_back(new Node(pre, '-', next));
			start.push(next);
			reChar.push('(');
			break;
		}
		case ')':
		{
			int ed = end.top();
			int st = start.top();
			trans.push_back(new Node(st, '-', ed));
			ch = reChar.top();
			while (ch != '(')
			{
				start.pop();
				reChar.pop();
				ch = reChar.top();
			}
			reChar.pop();
			reChar.push('#');
			start.pop();
			int newst = end.top();
			start.push(newst);
			end.pop();
			break;
		}
		case '|':
		{
			int ed = end.top();
			int st = start.top();
			trans.push_back(new Node(st, '-', ed));
			ch = reChar.top();
			while (ch != '('&&ch != '$')
			{
				start.pop();
				reChar.pop();
				ch = reChar.top();
			}
			start.pop();
			int pre = start.top();
			start.push(status++);
			int next = start.top();
			trans.push_back(new Node(pre, '-', next));
			break;
		}
		case '*':
		{
			int next = start.top();
			start.pop();
			int pre = start.top();
			trans.push_back(new Node(pre, '-', next));
			trans.push_back(new Node(next, '-', pre));
			start.push(next);
			break;
		}
		default:
		{
			reChar.push(ch);
			int pre = start.top();
			start.push(status++);
			int next = start.top();
			trans.push_back(new Node(pre, ch, next));
			break;
		}
		}
	}
	trans.push_back(new Node(start.top(), '-', end.top()));
}

void MyClass::printNFA()
{
	cout << "NFA:" << endl;
	for (auto node : trans)
		cout << node->pre << "--[" << node->input << "]-->" << node->next << endl;
}

vector<int> MyClass::closure(int s)
{
	vector<int> temp;
	vector<int> save;
	temp.push_back(s);
	save.push_back(s);
	while (!temp.empty())
	{
		int vec = temp.back();
		temp.pop_back();
		for (auto node : trans)
		{
			if (node->pre == vec && node->input == '-'&&count(save.begin(), save.end(), node->next) == 0)
			{
				temp.push_back(node->next);
				save.push_back(node->next);
			}
		}
	}
	sort(save.begin(), save.end());
	return save;
}

vector<int> MyClass::closure(vector<int> s)
{
	vector<int> temp=s;
	vector<int> save=s;
	while (!temp.empty())
	{
		int vec = temp.back();
		temp.pop_back();
		for (auto node : trans)
		{
			if (node->pre == vec && node->input == '-'&&count(save.begin(), save.end(), node->next) == 0)
			{
				temp.push_back(node->next);
				save.push_back(node->next);
			}
		}
	}
	sort(save.begin(), save.end());
	return save;
}

vector<int> MyClass::move(vector<int> T, char a)
{
	vector<int> temp;
	for (auto t : T)
	{
		for (auto node : trans)
		{
			if (node->pre == t && node->input == a)
				temp.push_back(node->next);
		}
	}
	sort(temp.begin(), temp.end());
	temp.erase(unique(temp.begin(), temp.end()), temp.end());
	return temp;
}

void MyClass::NFAToDFA()
{
	vector<vector<int>> temp;
	vector<vector<int>> save;
	temp.push_back(closure({ 0 }));
	save.push_back(closure({ 0 }));
	while (!temp.empty())
	{
		vector<int> vec = temp.back();
		temp.pop_back();
		if (!closure(move(vec, 'a')).empty())
		{
			DFA.push_back(new Dtran(vec, 'a', closure(move(vec, 'a'))));
			if (count(save.begin(), save.end(), closure(move(vec, 'a'))) == 0)
			{
				save.push_back(closure(move(vec, 'a')));
				temp.push_back(closure(move(vec, 'a')));
			}
		}
		if (!closure(move(vec, 'b')).empty())
		{
			DFA.push_back(new Dtran(vec, 'b', closure(move(vec, 'b'))));
			if (count(save.begin(), save.end(), closure(move(vec, 'b'))) == 0)
			{
				save.push_back(closure(move(vec, 'b')));
				temp.push_back(closure(move(vec, 'b')));
			}
		}
	}
	finish.resize(DFA.size());
	int num = 0;
	for (auto node : save)
	{
		int tmp = num++;
		if (count(node.begin(), node.end(), trans.back()->next) != 0)
			finish[tmp] = 1;
		for (auto dfa : DFA)
		{
			if (dfa->pre == node)
				dfa->pre = { tmp };
			if (dfa->next == node)
				dfa->next = { tmp };
		}
	}
}

void MyClass::printDFA()
{
	cout << "DFA:" << endl;
	for (auto d : DFA)
	{
		for (vector<int>::iterator iter = d->pre.begin(); iter != d->pre.end(); iter++)
			cout << *iter;
		cout << "--[" << d->input << "]-->";
		for (vector<int>::iterator iter = d->next.begin(); iter != d->next.end(); iter++)
			cout << *iter;
		cout << endl;
	}
}

void MyClass::accept(char a[])
{
	int last = 0;
	int temp = 0;
	for (int i = 0; i < strlen(a); i++)
	{
		int flag = 0;
		for (auto dfa : DFA)
		{
			if (dfa->pre[0] == last && dfa->input == a[i])
			{
				last = dfa->next[0];
				flag = 1;
				break;
			}
		}
		if (flag == 0)
		{
			cout << "不能接受该字符串！" << endl;
			return;
		}
	}
	if (finish[last] == 1)
		cout << "能接受该字符串！" << endl;
	else
		cout << "不能接受该字符串！" << endl;
}

int main()
{
	char a[20];
	string str;
	stack<int> stk;
	cout << "请输入正则表达式：";
	getline(cin, str);
	MyClass mc(str);
	mc.reToNFA();
	mc.printNFA();
	mc.NFAToDFA();
	mc.printDFA();
	cout << "请输入接受的字符串：";
	cin >> a;
	mc.accept(a);
}