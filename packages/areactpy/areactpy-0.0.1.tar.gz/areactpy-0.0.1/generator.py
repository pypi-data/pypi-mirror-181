import graphviz
import os

aws_icon_prefix = 'Arch_Amazon-'
aws_icon_suffix = '_32.png'
aws_icon_location = 'resource/all-icons/'

resources = [
    {
        "arn": "arn1",
        "label": "ec2"
    },
    {
        "arn": "arn2",
        "label": "ec2"
    },
    {
        "arn": "rds",
        "label": "rds"
    },
    {
        "arn": "alb",
        "label": "elasticloadbalancing"
    }
]
links = [
    {
        "from": "arn1",
        "to": "rds"
    },
    {
        "from": "arn2",
        "to": "rds"
    },
    {
        "from": "alb",
        "to": "arn1"
    },
    {
        "from": "alb",
        "to": "arn2"
    }
]

def get_icon_location(component):
    location = ''
    image_name = aws_icon_prefix + component.upper() + aws_icon_suffix
    for root, dirs, files in os.walk(aws_icon_location):
        for name in files:
            if name.__eq__(image_name):
                location = root + '/' + name
                print(location)
                break
    return location

def create_graph(nodes, edges, name):
    print('architecture diagram creation under process...')
    g = graphviz.Graph()
    for node in nodes:
        image_location = get_icon_location(node['label'])
        g.node(name = node['arn'], label = node['label'], shape = "plaintext", image = image_location)
    for edge in edges:
        g.edge(edge['from'], edge['to'])
    g.render(name)
    print('processing completed successfully!!!')

# main function
def main():
    # name of the graph ({product}-{env}-architecture-diagram)
    example_name = 'profilex-qa-architecture-diagram'
    create_graph(resources, links, example_name)

main()
