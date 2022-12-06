#include <iostream>
#include <queue>
#include <time.h>
using namespace std;

struct NODE
{
    int key;
    NODE *pLeft;
    NODE *pRight;
};

NODE *getMinimumNode(NODE *pRoot)
{
    NODE *node = pRoot;
    if (node != NULL)
    {
        while (node->pLeft != NULL)
        {
            node = node->pLeft;
        }
    }
    return node;
}
NODE *getMaximumNode(NODE *pRoot)
{
    NODE *node = pRoot;
    if (node != NULL)
    {
        while (node->pRight != NULL)
        {
            node = node->pRight;
        }
    }
    return node;
}
int getMinimumKey(NODE *pRoot)
{
    NODE *node = pRoot;
    if (node != NULL)
    {
        while (node->pLeft != NULL)
        {
            node = node->pLeft;
        }
    }
    return (node) ? node->key : 1e9;
}
int getMaximumKey(NODE *pRoot)
{
    NODE *node = pRoot;
    if (node != NULL)
    {
        while (node->pRight != NULL)
        {
            node = node->pRight;
        }
    }
    return (node) ? node->key : -1e9;
}
// 1. Initialize a NODE from a given value:
NODE *createNode(int data)
{
    NODE *node = new NODE;
    node->key = data;
    node->pLeft = NULL;
    node->pRight = NULL;
    return node;
}

// 2. Add a NODE with given value into a given Binary Search Tree:
void Insert(NODE *&pRoot, int x)
{
    if (pRoot == NULL)
    {
        pRoot = createNode(x);
        return;
    }
    else
    {
        if (pRoot->key > x)
        {
            Insert(pRoot->pLeft, x);
        }

        else
        {
            Insert(pRoot->pRight, x);
        }
    }
}

// 3. Pre-order Traversal:
void NLR(NODE *pRoot)
{
    if (pRoot != NULL)
    {
        cout << pRoot->key << " ";
        NLR(pRoot->pLeft);
        NLR(pRoot->pRight);
    }
}

// 4. In-order Traversal:
void LNR(NODE *pRoot)
{
    if (pRoot != NULL)
    {
        LNR(pRoot->pLeft);
        cout << pRoot->key << " ";
        LNR(pRoot->pRight);
    }
}
// 5. Post-order Traversal:
void LRN(NODE *pRoot)
{
    if (pRoot != NULL)
    {
        LRN(pRoot->pLeft);
        LRN(pRoot->pRight);
        cout << pRoot->key << " ";
    }
}
// 6. Level-order Traversal:
void LevelOrder(NODE *pRoot)
{
    if (pRoot == NULL)
        return;

    queue<NODE *> q;

    q.push(pRoot);

    while (q.empty() == false)
    {
        NODE *node = q.front();
        cout << node->key << " ";
        q.pop();

        if (node->pLeft != NULL)
            q.push(node->pLeft);

        if (node->pRight != NULL)
            q.push(node->pRight);
    }
}
// 7. Calculate the height of a given Binary Tree;
int Height(NODE *pRoot)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int lheight = Height(pRoot->pLeft);
        int rheight = Height(pRoot->pRight);

        if (lheight > rheight)
        {
            return (lheight + 1);
        }
        else
        {
            return (rheight + 1);
        }
    }
}

// 8. Count the number of NODE from a given Binary Tree:
int countNode(NODE *pRoot)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int countLeft = countNode(pRoot->pLeft);
        int countRight = countNode(pRoot->pRight);
        return countLeft + countRight + 1;
    }
}

// 9. Calculate the total value of all NODEs from a given Binary Tree:
int sumNode(NODE *pRoot)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int sumLeft = sumNode(pRoot->pLeft);
        int sumRight = sumNode(pRoot->pRight);
        return sumLeft + sumRight + pRoot->key;
    }
}

// 10. Find and return a NODE with given value from a given Binary Search Tree:
NODE *Search(NODE *pRoot, int x)
{
    if (pRoot == NULL)
        return NULL;

    else
    {
        if (pRoot->key > x)
        {
            return Search(pRoot->pLeft, x);
        }
        else if (pRoot->key < x)
        {
            return Search(pRoot->pRight, x);
        }
        else
        {
            return pRoot;
        }
    }
}
// 11. Remove a NODE with given value from a given Binary Search Tree:
void Remove(NODE *&pRoot, int x)
{
    NODE *parent = NULL, *curr = pRoot;
    while (curr != NULL && curr->key != x)
    {
        parent = curr;
        if (x < curr->key)
            curr = curr->pLeft;
        else
            curr = curr->pRight;
    }
    if (curr != NULL)
    {
        if (curr->pLeft == NULL && curr->pRight == NULL)
        {
            if (curr != pRoot)
            {
                if (parent->pLeft == curr)
                    parent->pLeft = NULL;
                else
                    parent->pRight = NULL;
                // curr = NULL;
            }
            else
                pRoot = NULL;
            free(curr);
        }

        else if (curr->pLeft && curr->pRight)
        {
            NODE *sucessor = getMinimumNode(curr->pRight);
            int value = sucessor->key;
            Remove(pRoot, sucessor->key);
            curr->key = value;
        }
        else
        {
            NODE *child = (curr->pLeft) ? curr->pLeft : curr->pRight;

            if (curr != pRoot)
            {
                if (curr == parent->pLeft)
                    parent->pLeft = child;
                else
                    parent->pRight = child;
            }

            else
                pRoot = child;
            free(curr);
        }
    }
}
// 12. Initialize a Binary Search Tree from a given array:
NODE *createTree(int a[], int n)
{
    NODE *pRoot = NULL;
    for (int i = 0; i < n; i++)
    {
        Insert(pRoot, a[i]);
    }
    return pRoot;
}
// 13. Completely remove a given Binary Search Tree:
void removeTree(NODE *&pRoot)
{
    if (pRoot != NULL)
    {
        removeTree(pRoot->pLeft);
        removeTree(pRoot->pRight);
        Remove(pRoot, pRoot->key);
    }
}
// 14. Calculate the height of a NODE with given value: (return -1 if value not exist)
int heightNode(NODE *pRoot, int value)
{
    NODE *node = Search(pRoot, value);
    return Height(node);
}
// 15. * Calculate the level of a given NODE:
int Level(NODE *pRoot, NODE *p)
{
    if (pRoot == NULL || p == NULL)
        return 0;
    if (p->key < pRoot->key)
    {
        int level = Level(pRoot->pLeft, p);
        return (level) ? level + 1 : level;
    }
    else if (pRoot->key < p->key)
    {
        int level = Level(pRoot->pRight, p);
        return (level) ? level + 1 : level;
    }
    else
        return 1;
}
// 16. * Count the number leaves from a given Binary Tree:
int countLeaf(NODE *pRoot)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int left = countLeaf(pRoot->pLeft);
        int right = countLeaf(pRoot->pRight);
        return (left || right) ? left + right : left + right + 1;
    }
}
// 17. * Count the number of NODE from a given Binary Search Tree which key value is less than a given
int countLess(NODE *pRoot, int x)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int countLeft = countLess(pRoot->pLeft, x);
        int countRight = countLess(pRoot->pRight, x);
        return (pRoot->key < x) ? countLeft + countRight + 1 : countLeft + countRight;
    }
}
// 18. * Count the number of NODE from a given Binary Search Tree which key value is greater than a given value:
int countGreater(NODE *pRoot, int x)
{
    if (pRoot == NULL)
        return 0;
    else
    {
        int countLeft = countGreater(pRoot->pLeft, x);
        int countRight = countGreater(pRoot->pRight, x);
        return (pRoot->key > x) ? countLeft + countRight + 1 : countLeft + countRight;
    }
}
// 19. * Determine if a given Binary Tree is Binary Search Tree:
bool isBST(NODE *pRoot)
{
    if (pRoot == NULL)
        return 1;

    int max_left = getMaximumKey(pRoot->pLeft);
    int min_right = getMinimumKey(pRoot->pRight);

    if (max_left > pRoot->key || min_right < pRoot->key)
        return 0;

    if (isBST(pRoot->pLeft) && isBST(pRoot->pRight))
        return 1;
    return 0;
}
// 20. * Determine if a given Binary Tree is a Full Binary Search Tree:
bool isFullBST(NODE *pRoot)
{
    if (pRoot == NULL)
        return 1;
    else
    {
        if (pRoot->pLeft != NULL && pRoot->pRight == NULL)
            return 0;

        if (pRoot->pLeft == NULL && pRoot->pRight != NULL)
            return 0;

        if (isFullBST(pRoot->pLeft) && isFullBST(pRoot->pRight))
            return 1;
        return 0;
    }
}
void InsertToTree(NODE *&pRoot, int x)
{
    if (pRoot == NULL)
    {
        pRoot = createNode(x);
        return;
    }
    else
    {
        if (pRoot->pLeft == NULL || pRoot->pRight != NULL)
            InsertToTree(pRoot->pLeft, x);
        else
            InsertToTree(pRoot->pRight, x);
    }
}
NODE *createRandomTree(int n)
{
    NODE *tree = NULL;
    int v;
    for (int i = 1; i <= n; i++)
    {
        int v = rand() % 50;
        InsertToTree(tree, v);
    }
    srand(time(NULL));
    return tree;
}
int main()
{
    srand(time(NULL));
    int arr[] = {41, 20, 65, 11, 29, 50, 91, 32, 72, 99};
    int n = sizeof(arr) / sizeof(arr[0]);
    int value = 17;
    NODE *a = createTree(arr, n);
    NODE *b = Search(a, value);
    NODE *c = createRandomTree(3);
    NODE *root = createNode(4);
    root->pLeft = new NODE;
    root->pLeft->key = 2;
    root->pRight = new NODE;
    root->pRight->key = 5;
    root->pLeft->pLeft = new NODE;
    root->pLeft->pLeft->key = 1;
    root->pLeft->pRight = new NODE;
    root->pLeft->pRight->key = 3;
    // Insert(a, 4);
    // Insert(a, 5);
    // Insert(a, 6);
    // Insert(a, 2);
    // Insert(a, 7);
    // Insert(a, 8);
    // Insert(a, 9);
    // Insert(a, 10);
    Remove(a, 91);
    cout
        << "Pre-order: ";
    NLR(a);
    cout << endl;
    cout << "In-order:";
    LNR(root);
    cout << endl;
    cout << "Level-order: ";
    LevelOrder(a);
    cout << endl
         << "Number of node: " << countNode(a) << endl
         << "Sum of all node: " << sumNode(a) << endl
         << "Height of tree: " << Height(a) << endl
         << "Height of node has key " << value << " : " << heightNode(a, value) << endl
         << "Level of node has key " << value << " : " << Level(a, b) << endl
         << "Number of node leaf: " << countLeaf(a) << endl
         << "Number of node which key value is less than " << value << " : " << countLess(a, value) << endl
         << "Number of node which key value is greater than " << value << " : " << countGreater(a, value) << endl;
    if (isBST(c))
        cout << "Is a binary search tree" << endl;
    else
        cout << "Is not a binary search tree" << endl;
    if (isFullBST(a))
        cout << "Is a full binary search tree" << endl;
    else
        cout << "Is not a full binary search tree" << endl;
    LNR(c);
    delete[] a;
    delete[] b;
    delete[] c;
    delete[] root;
    return 0;
}