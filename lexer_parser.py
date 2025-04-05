
import ply.lex as lex
import ply.yacc as yacc

# --------------------------
# Lexer
# --------------------------
tokens = (
    'LIST', 'BOOK', 'CONFIRM', 'PAY', 'CANCEL', 'VIEW',
    'CONCERT', 'FOOTBALL', 'TRAIN', 'AIRLINE', 'TICKETS',
    'FROM', 'TO', 'ON', 'AT', 'FOR', 'IN', 'MY', 'AREA',
    'DATE', 'TIME', 'STRING', 'MATCH', 'BOOKINGS', 'IDENTIFIER'
)

def t_LIST(t):
    r'[Ll][Ii][Ss][Tt]'
    return t

def t_BOOKINGS(t):
    r'[Bb][Oo][Oo][Kk][Ii][Nn][Gg][Ss]'
    return t

def t_BOOK(t):
    r'[Bb][Oo][Oo][Kk]'
    return t

def t_CONFIRM(t):
    r'[Cc][Oo][Nn][Ff][Ii][Rr][Mm]'
    return t

def t_PAY(t):
    r'[Pp][Aa][Yy]'
    return t

def t_CANCEL(t):
    r'[Cc][Aa][Nn][Cc][Ee][Ll]'
    return t

def t_VIEW(t):
    r'[Vv][Ii][Ee][Ww]'
    return t

def t_CONCERT(t):
    r'[Cc][Oo][Nn][Cc][Ee][Rr][Tt]'
    return t

def t_FOOTBALL(t):
    r'[Ff][Oo][Oo][Tt][Bb][Aa][Ll][Ll]'
    return t

def t_TRAIN(t):
    r'[Tt][Rr][Aa][Ii][Nn]'
    return t

def t_AIRLINE(t):
    r'[Aa][Ii][Rr][Ll][Ii][Nn][Ee]'
    return t

def t_TICKETS(t):
    r'[Tt][Ii][Cc][Kk][Ee][Tt][Ss]'
    return t

def t_MATCH(t):
    r'[Mm][Aa][Tt][Cc][Hh]'
    return t

def t_FROM(t):
    r'[Ff][Rr][Oo][Mm]'
    return t

def t_TO(t):
    r'[Tt][Oo]'
    return t

def t_ON(t):
    r'[Oo][Nn]'
    return t

def t_AT(t):
    r'[Aa][Tt]'
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr]'
    return t

def t_IN(t):
    r'[Ii][Nn]'
    return t

def t_MY(t):
    r'[Mm][Yy]'
    return t

def t_AREA(t):
    r'[Aa][Rr][Ee][Aa]'
    return t

def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    return t

def t_TIME(t):
    r'\d{2}:\d{2}'
    return t

def t_STRING(t):
    r'\"[^\"]+\"'
    t.value = t.value.strip('\"')
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z]+'
    t.value = t.value.lower()
    return t

t_ignore = ' \t'

def t_error(t):
    error_msg = f"Invalid character '{t.value[0]}'"
    t.lexer.skip(1)
    return error_msg

lexer = lex.lex()

# --------------------------
# Parser Rules
# --------------------------
def p_statement(p):
    """statement : list_command
                 | booking_command
                 | status_command
                 | view_command"""
    p[0] = p[1]

def p_list_command(p):
    """list_command : LIST event_type TICKETS IN MY AREA"""
    p[0] = ('LIST', p[2].lower())

def p_booking_command(p):
    """booking_command : book_transport
                      | book_event"""
    p[0] = p[1]

def p_book_transport(p):
    """book_transport : BOOK TRAIN FROM location TO location ON DATE AT TIME FOR person
                     | BOOK AIRLINE FROM location TO location ON DATE AT TIME FOR person"""
    p[0] = ('BOOK', {
        'type': p[2].lower(),
        'from': ' '.join(p[4]),
        'to': ' '.join(p[6]),
        'date': p[8],
        'time': p[10],
        'person': ' '.join(p[12])
    })

def p_book_event(p):
    """book_event : BOOK event_name CONCERT FOR person
                 | BOOK event_name FOOTBALL MATCH FOR person"""
    p[0] = ('BOOK', {
        'type': p[3].lower(),
        'name': ' '.join(p[2]),
        'person': ' '.join(p[5]) if p[3].lower() == 'concert' else ' '.join(p[6])
    })

def p_status_command(p):
    """status_command : CONFIRM event_type FOR person
                      | PAY event_type FOR person
                      | CANCEL event_type FOR person"""
    p[0] = (p[1].upper(), {
        'type': p[2],
        'person': ' '.join(p[4])
    })

def p_view_command(p):
    """view_command : VIEW BOOKINGS"""
    p[0] = ('VIEW', {'action': 'show_bookings'})

def p_event_type(p):
    """event_type : CONCERT
                 | FOOTBALL
                 | TRAIN
                 | AIRLINE"""
    p[0] = p[1].lower()

def p_location(p):
    """location : IDENTIFIER
               | STRING
               | location IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_person(p):
    """person : IDENTIFIER
             | STRING
             | person IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_event_name(p):
    """event_name : IDENTIFIER
                 | STRING
                 | event_name IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_error(p):
    if p:
        error_msg = f"Syntax error at '{p.value}'"
    else:
        error_msg = "Syntax error at end of input"
    return error_msg

parser = yacc.yacc()