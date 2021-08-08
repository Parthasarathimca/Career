class MatType(object):
    '''
    Choices for Material type
    '''
    PBI_MEL_2_SIDE = 1
    FORMALDEHYDE_FREE_PBI_MEL_2_SIDE = 2
    PBI_TEXTURED = 3
    PBI_SEMI_TEXTURED = 4
    PBI_MEL_2_SIDE_4X10 = 5
    PBI_MEL_TEXTURED_4X10 = 6
    OTHER = 7

    MAT_TYPE_CHOICES = (
        (PBI_MEL_2_SIDE, '3/4 PBI Mel 2 side'),
        (FORMALDEHYDE_FREE_PBI_MEL_2_SIDE, '3/4 Formaldehyde Free PBI Mel 2 side'),
        (PBI_TEXTURED, '3/4 PBI Textured'),
        (PBI_SEMI_TEXTURED, '3/4 PBI Semi Textured'),
        (PBI_MEL_2_SIDE_4X10, '3/4 PBI Mel 2 side 4X10'),
        (PBI_MEL_TEXTURED_4X10, '3/4 PBI Mel Textured 4X10'),
        (OTHER, 'Other')
    )

class Colors(object):
    '''
    All the available bd colors with codes
    '''
    WHITE = '#FFF'
    BLACK = '#000000'
    RED = '#FF0000'
    BLUE = '#0000FF'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'
    LIME = '#00FF00'
    PINK = '#FFC0CB'
    MAGENTA = '#FF00FF'
    EMERALD = '#50C878'

    COLOR_CHOICES = (
        (WHITE, 'White'),        
        (BLACK, 'Black'),
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (PURPLE, 'Purple'),
        (YELLOW, 'Yellow'),
        (LIME, 'Lime'),
        (PINK, 'Pink'),
        (MAGENTA, 'Magenta'),
        (EMERALD, 'Emerald'),
    )
