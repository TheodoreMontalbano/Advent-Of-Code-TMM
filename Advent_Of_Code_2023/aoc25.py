def get_ans(data):
    graph = create_graph(format_data(data))
    for i in graph.keys():
        if i == "Head":
            continue
        graph["Head"] = i
        cut = get_cut(graph, 3)
        if len(cut.keys()) + 1 < len(graph.keys()):
            # Subtract an extra one because of "Head"
            return len(cut.keys()) * (len(graph.keys()) - len(cut.keys()) - 1)
    return -1


# Assumes we know the size of the min cut
def get_cut(graph, wanted_cut_size):
    cut = {graph["Head"]: 1}
    curr_connections = {}
    for i in graph[graph["Head"]]:
        curr_connections[i] = 1
    while not get_graph_out_degree(graph, cut) == wanted_cut_size and len(graph.keys()) > len(cut.keys()) + 1:
        curr_min_out_degree = len(graph.keys())
        curr_min_node = ""
        for i in curr_connections.keys():
            cut[i] = 1
            curr_degree = get_graph_out_degree(graph, cut)
            if curr_degree <= curr_min_out_degree:
                curr_min_out_degree = curr_degree
                curr_min_node = i
            cut.pop(i)
        curr_connections.pop(curr_min_node)
        cut[curr_min_node] = 1
        for i in graph[curr_min_node]:
            if i not in cut:
                curr_connections[i] = 1
    return cut


def format_data(data):
    str_arr = data.split("\n")
    graph_data = []
    for i in str_arr:
        curr = i.split(":")
        graph_data.append([curr[0], curr[1].split(" ")[1:]])
    return graph_data


def get_graph_out_degree(full_graph, graph_cut):
    count = 0
    for i in graph_cut.keys():
        for j in full_graph[i]:
            if j not in graph_cut:
                count = count + 1
    return count


def add_connection(node_one, node_two, graph):
    if node_one in graph:
        graph[node_one].append(node_two)
    else:
        graph[node_one] = [node_two]
    if node_two in graph:
        graph[node_two].append(node_one)
    else:
        graph[node_two] = [node_one]


def create_graph(graph_data):
    graph = {}
    for i in graph_data:
        curr = i[0]
        for j in i[1]:
            add_connection(curr, j, graph)
    graph["Head"] = graph_data[0][0]
    return graph
