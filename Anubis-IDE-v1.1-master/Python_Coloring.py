from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

#this is a variable to carry the file extension for later comparison
global extension
extension = ""

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES2 = {
    'keyword': format([200, 120, 50], 'bold'),
    'operator': format([150, 150, 150]),
    'brace': format('darkGray'),
    'defclass': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'string2': format([30, 120, 110]),
    'comment': format([128, 128, 128]),
    'self': format([150, 85, 140], 'italic'),
    'numbers': format([100, 150, 190]),
}
STYLES = {
       'keyword': format('blue'),
      'operator': format('red'),
       'brace': format('darkGray'),
       'defclass': format('black', 'bold'),
       'string': format('magenta'),
       'string2': format('darkMagenta'),
       'comment': format('darkGreen', 'italic'),
       'self': format('black', 'italic'),
       'numbers': format('brown'),
   }

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    Pykeywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # C# keywords
    CSharpKeywords = ['var','abstract'     ,'as'     ,'base'     ,'bool'
        ,'break'     ,'byte'     ,'case'     ,'catch'
        ,'char'     ,'checked'     ,'class'     ,'const'
        ,'continue'     ,'decimal'     ,'default'     ,'delegate'
        ,'do' ,    'double'     ,'else'     ,'enum'
        ,'event'     ,'explicit'     ,'extern'     ,'false'
        ,'finally'     ,'fixed'     ,'float'     ,'for'
        ,'foreach'     ,'goto'     ,'if'     ,'implicit'
        ,'in'     ,'int'     ,'interface'     ,'internal'
        ,'is'     ,'lock'     ,'long'     ,'namespace'
        ,'new'     ,'null'     ,'object'     ,'operator'
        ,'out'     ,'override'     ,'params'     ,'private'
        ,'protected'     ,'public'     ,'readonly' ,    'ref'
        ,'return'     ,'sbyte'     ,'sealed'     ,'short',
        'sizeof'     ,'stackalloc'     ,'static'     ,'string'
        ,'struct'     ,'switch'     ,'this'     ,'throw'
        ,'true'     ,'try'     ,'typeof'     ,'uint'
        ,'ulong'     ,'unchecked'     ,'unsafe'     ,'ushort'
        ,'using'     ,'virtual'     ,'void'     ,'volatile'
        ,'while']

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])
        self.CSmulticomment = (QRegExp('/\*'), QRegExp('\*/'),  3, STYLES['comment'])

        Pyrules = []
        CSrules = []

        # Keyword, operator, and brace rules
        Pyrules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.Pykeywords]
        Pyrules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in PythonHighlighter.operators]
        Pyrules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in PythonHighlighter.braces]

        # C# rules
        CSrules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                    for w in PythonHighlighter.CSharpKeywords]
        CSrules += [(r'%s' % o, 0, STYLES['operator'])
                    for o in PythonHighlighter.operators]
        CSrules += [(r'%s' % b, 0, STYLES['brace'])
                    for b in PythonHighlighter.braces]

        # All other rules
        Pyrules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        CSrules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),



            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '//' until a newline
            (r'//[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.Pyrules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in Pyrules]

        #rules for C#
        self.CSrules = [(QRegExp(pat), index, fmt)
                             for (pat, index, fmt) in CSrules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """

        #if any extension other than .py and .cs then do not format
        if extension != ".py" and extension != ".cs":
            return


#_________python extension found_____________________________________________________________________________
        elif extension == ".py":
            # Do other syntax formatting
            for expression, nth, format in self.Pyrules:
                index = expression.indexIn(text, 0)

                while index >= 0:
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

            # Do multi-line strings
            in_multiline = self.match_multiline(text, *self.tri_single)
            if not in_multiline:
                in_multiline = self.match_multiline(text, *self.tri_double)

#_______C# extension found________________________________________________________________________________
        elif extension == ".cs":
            # Do other syntax formatting
            for expression, nth, format in self.CSrules:
                index = expression.indexIn(text, 0)

                while index >= 0:
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

            # Do multi-line strings
            in_multiline = self.match_multiline_CS(text, *self.CSmulticomment)


    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


    #for multiline comments in CS we do the following
    def match_multiline_CS(self, text, starter, delimiter, in_state, style):

        # If inside the comments, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the starter (/*) on this line
        else:
            start = starter.indexIn(text)
            # Move past this match
            add = starter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False