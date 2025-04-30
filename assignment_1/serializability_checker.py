from collections import defaultdict


def parse_history(history_str):
    tokens = history_str.strip().split()
    operations = []
    i = 0
    while i < len(tokens):
        op = tokens[i]
        tid = int(tokens[i + 1])
        item = tokens[i + 2]
        operations.append((op, tid, item))
        i += 3
    return operations

def build_precedence_graph(operations):
    graph = defaultdict(set)
    transactions = set()
    
    for i in range(len(operations)):
        op1, tid1, item1 = operations[i]
        transactions.add(tid1)
        for j in range(i + 1, len(operations)):
            op2, tid2, item2 = operations[j]
            transactions.add(tid2)
            if tid1 != tid2 and item1 == item2:
                if (op1 == 'r' and op2 == 'w') or \
                    (op1 == 'w' and op2 == 'r') or \
                        (op1 == 'w' and op2 == 'w'):
                            graph[tid1].add(tid2)     
    return graph, transactions
    
def has_cycle(graph, transactions):
    visited = set()
    stack = set()
    
    def dfs(tid):
        visited.add(tid)
        stack.add(tid)
        for neighbour in graph[tid]:
            if neighbour not in visited:
                if dfs(neighbour):
                    return True
            elif neighbour in stack:
                return True
        stack.remove(tid)
        return False
    
    for tid in transactions:
        if tid not in visited:
            if dfs(tid):
                return True
    return False

def main():
    history_input = input("Enter history (e.g., 'w 1 x r 2 x w 2 y r 3 y w 3 z r 1 z'):\n")
    operations = parse_history(history_input)
    graph, transactions = build_precedence_graph(operations)
    cycle = has_cycle(graph, transactions)
    
    print("false" if cycle else "true")
    
if __name__ == "__main__":
    main()

