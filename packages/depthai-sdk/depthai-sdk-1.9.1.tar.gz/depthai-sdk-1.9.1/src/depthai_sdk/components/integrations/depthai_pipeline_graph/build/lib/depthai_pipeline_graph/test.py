from Qt import QtWidgets, QtCore
from NodeGraphQt import NodeGraph, BaseNode, PropertiesBinWidget, Port
import time

# create a node class object inherited from BaseNode.
class FooNode(BaseNode):

    # unique node identifier domain.
    __identifier__ = 'com.chantasticvfx'

    # initial default node name.
    NODE_NAME = 'Foo Node'

    def __init__(self):
        super(FooNode, self).__init__()

        # create an input port.
        self.add_input('in')

        # create an output port.
        self.add_output('out')


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(["DepthAI Pipeline Graph"])

    # create node graph controller.
    graph = NodeGraph()

    # set up default menu and commands.
    # setup_context_menu(graph)

    # register the FooNode node class.
    graph.register_node(FooNode)

    # show the node graph widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)

    properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # show the node properties bin widget when a node is double clicked.
    def display_properties_bin(node):
        global properties_bin
        if not properties_bin.isVisible():
            properties_bin.show()

    # wire function to "node_double_clicked" signal.
    graph.node_double_clicked.connect(display_properties_bin)

    # create two nodes.
    node_a = graph.create_node('com.chantasticvfx.FooNode', name='node A')
    output = node_a.add_output(name='out1')
    node_b = graph.create_node('com.chantasticvfx.FooNode', name='node B', pos=(300, 50))
    input = node_b.add_input(name='in1')

    link = input.connect_to(output)

    graph.widget.show()


    while True:
        time.sleep(0.1)
        link.new_event(sender=True)
        link.new_event(sender=True)
        link.new_event(sender=False)
        # output.view.name = str(i)
        app.processEvents()

    app.exec_()