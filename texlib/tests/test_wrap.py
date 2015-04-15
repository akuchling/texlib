
import sys
import unittest
from texlib import wrap

class TestGlueClass(unittest.TestCase):
    def test_stretch(self):
        glue = wrap.Glue(10, stretch=5, shrink=2)

        self.assertEqual(glue.compute_width(r=0), 10)
        self.assertEqual(glue.compute_width(r=-1), 8)
        self.assertEqual(glue.compute_width(r=1), 15)
        self.assertEqual(glue.compute_width(r=-0.5), 9)
        self.assertEqual(glue.compute_width(r=+0.5), 12.5)


class TestObjectList(unittest.TestCase):
    def test_list_behaviour(self):
        # Verify that ObjectList behaves like a Python list
        ol = wrap.ObjectList()
        self.assertEqual(len(ol), 0)

        ol.append(wrap.Glue(0, 1, 0))
        self.assertEqual(len(ol), 1)

        ol.append(ol[0])
        self.assertEqual(len(ol), 2)

        del ol[1:]
        self.assertEqual(len(ol), 1)

        ol.pop(0)
        self.assertEqual(len(ol), 0)

    def assemble_paragraph(self, text):
        """Turn a paragraph of text into an ObjectList.

        '@' indicates a forced line break.
        """
        # Normalize the text
        text = ' '.join(text.split())
        L = wrap.ObjectList()
        for ch in text:
            if ch in ' \n':
                # Append interword space -- 2 units +/- 1
                L.append( wrap.Glue(2,1,1) )
            elif ch == '@':
                # Append forced break
                L.append( wrap.Penalty(0, -wrap.INFINITY) )
            else:
                # All characters are 1 unit wide
                b = wrap.Box(1, ch)
                L.append( b )

        # Append closing penalty and glue
        L.add_closing_penalty()
        return L

    def output(self, ol, line_lengths, breaks, full_justify=False):
        """Output a properly wrapped version of some text.

        :param ol:           ObjectList containing some text
        :param breakpoints:  list containing indexes of where line breaks should occur
        :param full_justify: if true, do full justification in the output
        """
        line_start = 0
        line = 0
        for breakpoint in breaks[1:]:
            r = ol.compute_adjustment_ratio(line_start, breakpoint, line, line_lengths)
            line = line + 1
            for i in range(line_start, breakpoint):
                box = ol[i]
                if box.is_glue():
                    if full_justify:
                        width = int( box.compute_width(r) )
                    else:
                        width = 1
                    sys.stdout.write(' '*width)

                elif box.is_box():
                    sys.stdout.write( box.character )
                else:
                    # We don't need to do anything for Penalty instances.
                    pass

            line_start = breakpoint + 1
            sys.stdout.write('\n')

        print

    def test_basic_wrap(self):
        text = """Writing this summary was difficult, because there were no large themes
        in the last two weeks of discussion.  Instead there were lots and lots
        of small items; as the release date for 2.0b1 nears, people are
        concentrating on resolving outstanding patches, fixing bugs, and
        making last-minute tweaks.
        Computes an Adler-32 checksum of string.  (An Adler-32
        checksum is almost as reliable as a CRC32 but can be computed much
        more quickly.)  If value is present, it is used as the
        starting value of the checksum; otherwise, a fixed default value is
        used.  This allows computing a running checksum over the
        concatenation of several input strings.  The algorithm is not
        cryptographically strong, and should not be used for
        authentication or digital signatures."""
        L = self.assemble_paragraph(text)

        line_width = 100                    # Line width to use for formatting
        line_lengths = [line_width]

        # Compute the breakpoints
        breaks = L.compute_breakpoints(line_lengths, tolerance = 2)
        self.assertEqual(breaks, [0, 95, 193, 288, 386, 486, 586, 686, 749])
        self.assertEqual(breaks[0], 0)
        ##self.output(L, line_lengths, breaks)


if __name__ == '__main__':
    unittest.main()
