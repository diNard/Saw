import unittest
from saw.parsers.words import Node, Words
from saw.parsers.blocks import Blocks
from saw.saw import Saw


class TestLoad(unittest.TestCase):
    def setUp(self):
        pass

    def test_type(self):
        node = Words.load('aa')
        self.assertEqual(node.type(), 'words')

        node.type('test')
        self.assertEqual(node.type(), 'test')

        self.assertEqual(node.type('none'), node)

    def test_before(self):
        node = Node()

        node.before([',', ':', '.'])
        self.assertEqual(node.before(), [',', ':', '.'])

        node.before('-', True).before('!', True)
        self.assertEqual(node.before(), [',', ':', '.', '-', '!'])

        self.assertEqual(node.before(['.', '-']), node)
        self.assertEqual(node.before(['.', '-'], True), node)

    def test_after(self):
        node = Node()

        node.after([',', ':', '.'])
        self.assertEqual(node.after(), [',', ':', '.'])

        node.after('-', True).after('!', True)
        self.assertEqual(node.after(), [',', ':', '.', '-', '!'])

        self.assertEqual(node.after(['.', '-']), node)
        self.assertEqual(node.after(['.', '-'], True), node)

    def test_text(self):
        node = Node()

        node.text('Any text')
        self.assertEqual(node.text(), 'Any text')

        node.text(', second', True).text(', third', True)
        self.assertEqual(node.text(), 'Any text, second, third')

        self.assertEqual(node.text('test'), node)
        self.assertEqual(node.text('test', True), node)

    def test___repr(self):
        node = Blocks.load('Test it, after that!')
        expect = {
            '_type': 'blocks', 
            '_': [{
                    '_type': 'words', 
                    '_after': [','], 
                    '_': [
                        {'_text': 'Test'}, 
                        {'_text': 'it'}
                    ]
                }, {
                    '_type': 'words', 
                    '_': [ 
                        {'_text': 'after'}, 
                        {'_text': 'that!'}
                    ]
                }
            ]
        }
        self.assertEqual(repr(node), repr(expect))

    def test__noexists_method(self):
        # @TODO
        pass

    def test__init_from_different_source(self):
        # @TODO
        pass

    def test___str(self):
        text = 'Any text, :yep:. Test it- test it fast?!'
        node = Saw.load(text)
        self.assertEqual(str(node), text)

    def test___getattr(self):
        # call List (main) method
        node1 = Words.load('first text')
        node2 = Words.load('second text')
        node3 = Words.load('first text second text')
        node1.extend(node2)
        self.assertEqual(node1, node3)

        # call method from List, that exists in String
        node = Saw.load('I like dogs, dogs very nice. I told that dogs anytime!')
        ###self.assertEqual(node3.words.count('text'), 2)
        
        node = Blocks.load('Any long, and terrible text; Just for test.')

        # call filter
        self.assertEqual(str(node.pure()), 'Any long and terrible text Just for test.')

        # call String methods
        self.assertEqual(node.islower(), False)
        self.assertEqual(node.replace('r', '_'), 'Any long, and te__ible text; Just fo_ test.')
        self.assertEqual(node.split(' '), ['Any', 'long,', 'and', 'terrible', 'text;', 'Just', 'for', 'test.'])

        # call alias
        self.assertEqual(node.blocks, node)

        # call children
        words_node = Words.load('Any long and terrible text Just for test.')
        self.assertEqual(node.words, words_node)

    def test___getitem(self):
        node = Blocks.load('Any text, second, third')

        self.assertEqual(node[0].__class__, Node)
        self.assertEqual(node[2].__class__, Node)

        self.assertEqual(node[0].type(), Words.type())
        self.assertEqual(node[2].type(), Words.type())

    def test___getslice(self):
        node = Words.load('Any text, second, third')

        sl_1 = node[:3]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), node.type())
        self.assertEqual(sl_1, Words.load('Any text, second,'))

        sl_2 = node[1:3]
        self.assertEqual(sl_2.__class__, Node)
        self.assertEqual(sl_2.type(), node.type())
        self.assertEqual(sl_2, Words.load('text, second,'))

        sl_3 = node[1:]
        self.assertEqual(sl_3.__class__, Node)
        self.assertEqual(sl_3.type(), node.type())
        self.assertEqual(sl_3, Words.load('text, second, third'))

        # old syntax by __getitem__
        sl_4 = node.__getitem__(slice(1,3))
        self.assertEqual(sl_4, sl_2)

    def test_get_item_and_slice(self):
        node = Blocks.load('Any advanced text, second, third')

        sl_1 = node[:3][2]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), Words.type())
        self.assertEqual(sl_1, Words.load('third'))

        sl_1 = node[0][:2]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), Words.type())
        self.assertEqual(sl_1, Words.load('Any advanced'))

    def test___eq(self):
        node = Blocks.load('*Any advanced text,')
        blocks = Node().type(Blocks.type())
        blocks.append(Node())

        block = blocks[0]
        self.assertNotEqual(blocks, node)
        block.before(['*'])
        self.assertNotEqual(blocks, node)
        block.after([','])
        self.assertNotEqual(blocks, node)
        block.type(Words.type())
        self.assertNotEqual(blocks, node)

        for word in Words.load('Any advanced text'):
            block.append(word)
        self.assertEqual(blocks, node)

    def test_copy(self):
        txt = 'Any text, yep. Test it!'
        sw = Blocks.load(txt)
        for a in sw.copy().words:
            a.text('_', True)

        self.assertEqual(str(sw), txt)


if __name__ == "__main__":
    unittest.main()