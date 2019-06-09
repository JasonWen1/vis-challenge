# coding:utf-8
import json
import numpy as np
import plotly.graph_objs as go

with open('HKUST_coauthor_graph.json', mode='r', encoding='utf-8') as f:
    data = json.load(f)

nodes = [node for node in data['nodes'] if node['dept'] == 'CSE']
nodes_id = [node['id'] for node in nodes]
nodes_postion = {node['id']: np.random.normal(loc=0.5, scale=0.01, size=2) for node in nodes}
nodes_name = {node['id']: node['fullname'] for node in nodes}
nodes_name_instead = {v: k for k, v in nodes_name.items()}

edges = {node_id: set() for node_id in nodes_id}
for edge in data['edges']:
    if (edge['source'] in nodes_id) and (edge['target'] in nodes_id):
        edges[edge['source']].add(edge['target'])
        edges[edge['target']].add(edge['source'])

edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.2, color='#D5D5D5'), hoverinfo='none', mode='lines')
for source_node, target_nodes in edges.items():
    for target_node in target_nodes:
        x0, y0 = nodes_postion.get(source_node)
        x1, y1 = nodes_postion.get(target_node)
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', marker=dict(
    showscale=False, colorscale='YlOrRd', reversescale=True, color=[], size=10, line=dict(width=2)
))
for node_id in nodes_id:
    x, y = nodes_postion.get(node_id)
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

for source_node, target_nodes in edges.items():
    node_trace['marker']['color'] += tuple([len(target_nodes)])
    node_info = f'fullname: {nodes_name.get(source_node)}; connections: {len(target_nodes)}'
    node_trace['text'] += tuple([node_info])

fig_node_link = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        clickmode='event+select',
        height=600,
        width=800,
        showlegend=False,
        hovermode='closest',
        margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
)

map_data = np.zeros(shape=(len(nodes_id), len(nodes_id)), dtype=np.float32)
for edge in data['edges']:
    if (edge['source'] in nodes_id) and (edge['target'] in nodes_id):
        map_data[nodes_id.index(edge['source']), nodes_id.index(edge['target'])] += 1
        map_data[nodes_id.index(edge['target']), nodes_id.index(edge['source'])] += 1

ticks = [nodes_name.get(node_id) for node_id in nodes_id]
fig_matrix = go.Figure(
    data=[
        go.Heatmap(
                x=ticks, y=ticks, z=map_data, hovertemplate='',
                reversescale=True, name='', xgap=2, ygap=2, showscale=True,
                colorscale=[(0, '#e70b0b'), (0.25, '#ff99ad'), (0.5, '#008B00'), (0.75, '#ffffff'), (1, '#f7f7f7')],
            ),
    ],
    layout=go.Layout(
            xaxis=dict(showline=True, showgrid=False, tickfont=dict(size=8)),
            yaxis=dict(showline=True, showgrid=False, tickfont=dict(size=8)),
            height=650, width=650,
    )
)


def update_matrix(hover_node):
    if not hover_node:
        return
    try:
        fullname, connections = hover_node['points'][0]['text'].split('; ')
        if connections[13:] == '0':
            return
        node_id = nodes_name_instead.get(fullname[10:])
        node_id_index = nodes_id.index(node_id)
    except KeyError:
        return

    map_data_tmp = map_data.copy()
    for x_index in range(len(nodes_id)):
        for y_index in range(x_index, len(nodes_id)):
            if x_index == node_id_index or y_index == node_id_index:
                continue
            else:
                map_data_tmp[x_index, y_index] = 0.75 if map_data[x_index, y_index] == 1 else 0.25
                map_data_tmp[y_index, x_index] = 0.75 if map_data[y_index, x_index] == 1 else 0.25

    fig_matrix_tmp = go.Figure(
        data=[
            go.Heatmap(
                x=ticks, y=ticks, z=map_data_tmp, hovertemplate='',
                reversescale=True, name='', xgap=2, ygap=2, showscale=True,
                colorscale=[(0, '#e70b0b'), (0.25, '#ff99ad'), (0.5, '#008B00'), (0.75, '#ffffff'), (1, '#f7f7f7')],
            ),
        ],
        layout=go.Layout(
            xaxis=dict(showline=True, showgrid=False, tickfont=dict(size=8)),
            yaxis=dict(showline=True, showgrid=False, tickfont=dict(size=8)),
            height=650, width=650,

        )
    )
    return fig_matrix_tmp


def update_node(hoverData):
    if not hoverData:
        return

    node1, node2, z = hoverData['points'][0]['x'], hoverData['points'][0]['y'], hoverData['points'][0]['z']
    if z <= 0.5:
        return

    node_id1, node_id2 = nodes_name_instead.get(node1), nodes_name_instead.get(node2)

    edge_trace_tmp = go.Scatter(x=[], y=[], line=dict(width=0.8, color='#DD2222'), hoverinfo='none', mode='lines')
    x0_tmp, y0_tmp = nodes_postion.get(node_id1)
    x1_tmp, y1_tmp = nodes_postion.get(node_id2)
    edge_trace_tmp['x'] += tuple([x0_tmp, x1_tmp, None])
    edge_trace_tmp['y'] += tuple([y0_tmp, y1_tmp, None])

    node_trace_tmp = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', marker=dict(
        showscale=False, colorscale='YlOrRd', reversescale=True, color=[], size=15, line=dict(width=2)
    ))
    for node_id in [node_id1, node_id2]:
        x_tmp, y_tmp = nodes_postion.get(node_id)
        node_trace_tmp['x'] += tuple([x_tmp])
        node_trace_tmp['y'] += tuple([y_tmp])

    for source_node_tmp in [node_id1, node_id2]:
        target_nodes_tmp = edges.get(source_node_tmp)
        node_trace_tmp['marker']['color'] += tuple([len(target_nodes_tmp)])
        node_info_tmp = f'fullname: {nodes_name.get(source_node_tmp)}; connections: {len(target_nodes_tmp)}'
        node_trace_tmp['text'] += tuple([node_info_tmp])

    fig_node_link_tmp = go.Figure(
        data=[edge_trace, node_trace, edge_trace_tmp, node_trace_tmp],
        layout=go.Layout(
            clickmode='event+select',
            height=600,
            width=800,
            showlegend=False,
            hovermode='closest',
            margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    return fig_node_link_tmp
