import boto3
import graphviz
import os

aws_icon_prefix = 'Arch_Amazon-'
aws_icon_suffix = '_32.png'
aws_icon_location = 'resource/all-icons/'
aws_tag_product = 'product'
aws_tag_environment = 'environment'

def get_resources_list():
    cloud_provider = input("enter your cloud provider name : ")
    cloud_region = input("enter your cloud region code : ")
    environment = input("enter your stack environment : ")
    product = input("enter your product name : ")
    client = boto3.client('resourcegroupstaggingapi', region_name=cloud_region)
    response = client.get_resources(
        TagFilters=[
            {
                'Key': aws_tag_product,
                'Values': [
                    product
                ],
                'Key': aws_tag_environment,
                'Values': [
                    environment
                ]
            }
        ]
    )
    resources = []
    for services in response['ResourceTagMappingList']:
        arn = services['ResourceARN']
        resource = {}
        resource['arn'] = arn
        resource['label'] = arn.split(":")[2]
        resources.append(resource)
    print(resources)
    return resources

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

def main():
    resources = get_resources_list()
    example_name = 'architecture-diagram'
    create_graph(resources, [], example_name)