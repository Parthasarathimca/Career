class DepthInches(object):
    '''
    Choices for Depth Inches
    '''
    TWELVE_INCH = 1
    SIXTEEN_INCH = 2
    TWENTY_FOUR_INCH = 3


    DEPTH_INCHES_CHOICES = (
        (TWELVE_INCH, '12'),
        (SIXTEEN_INCH, '16'),
        (TWENTY_FOUR_INCH, '24'),

    )

class EdgeProfile(object):
    '''
    Edge Profile For Room Partition
    '''

    FLAT = 1
    ROUND = 2

    EDGE_PROFILE_CHOICES = (
        (FLAT, 'Flat'),
        (ROUND, 'Round')
    )

class DogEared(object):
    '''
    Dog Eared Choices In Partion Form 
    '''

    NO_DOG = 1
    DOG_EARED_12 = 2
    DOG_EARED_16 = 3

    DOG_EARED_CHOICES = (
        (NO_DOG, 'No Dogear'),
        (DOG_EARED_12, 'Dog Eared to 12"'),
        (DOG_EARED_16, 'Dog Eared to 16"')
    )


class Description(object):
    PARTITION = "Partition"
    KD_SHELF = "KD Shelf"
    IN_KD_SHELF = "1in KD Shelf"
    SINGLE_DOOR = "Door (Single)"
    PAIR_DOOR = "Pair Doors"
    ADJ_SHELF = "Adj Shelf"
    IN_ADJ_SHELF = "1in Adj Shelf"
    SHOE_SHELF = "Show Shelf"
    DRAWER_BOX = "Drawer Box"
    CUSTOM_SHELF = 'Custom Shelf'
    CLEAT = 'Cleats'
    TOE_KICK = 'Toe Kick'
    l_SHELF='L-SHELF'
    CORNER_SHELF='CORNER-SHELF'
    TOP_SHELF='TOP_SHELF'
    DRAWER_FACES='DRAWER FACES'
    

PARTITION_DRILL_CHOICES = [100100,10050]

PARTITION_MAT_CHOICES = [15000,15205]


DRAWER_TYPE_CHOICES = (('', 'Select Category'), ('CUSTOM', 'CUSTOM'), ('STANDARD', 'STANDARD'))
drawer_size = [2.00, 3.94, 5.20, 6.46, 7.72, 8.98, 10.24]

DRAWER_SIZE_CHOICES =(
    ("4H", "4H"),
    ("5H", "5H"),
    ("6H", "6H"),
    ("7H", "7H"),
    ("8H", "8H"),
    ("9H", "9H"),
    ("10H", "10H"),
)
CLEAT_WIDTH_CHOICES =(
    (0, "Select Width"),
    (12.00, "12''"),
    (15.00, "15''"),
    (18.00, "18''"),
    (21.00, "21''"),
    (24.00, "24''"),
    (27.00, "27''"),
    (30.00, "30''"),
    (33.00, "33''"),
    (36.00, "36''"),
    (39.00, "39''"),
    (42.00, "42''"),
    (45.00, "45''"),
    (48.00, "48''"),
)

PARTTION_HEIGHT_CHOICES = (
    (25.94, "25.94'' (20H)"),
    (30.98, "30.98'' (24H)"),
    (36.02, "36.02'' (28H)"),
    (47.37, "47.37'' (37H)"),
    (54.92, "54.92'' (43H)"),
    (59.96, "59.96'' (47H)"),
    (77.60, "77.60'' (61H)"),
    (78.86, "78.86'' (62H)"),
    (80.12, "80.12'' (63H)"),
    (90.20, "90.20'' (71H)"),
)

PARTTION_DEPTH_CHOICES = (
    (12.00, "12''"),
    (16.00, "16''"),
    (24.00, "24''"),
)


class MTChoices(object):

    PARTION_MT_CHOICES = (
        (1, "Mel"),
        (2, "P/B"),
    )



CLEAT_EXPOSED_END_CHOICES = (
        ("none", "None"),
        ("single", "Single Exposed Ends"),
        ("both", "Both Exposed Ends"),
        ("edgeband", "Edgeband All 4 sizes (Robe Hook Cleat)"),
    )


FACE_COLOR_CHOICES = (

        ("main", "Main"),
        ("doorndrawer", "Door'' n Drawer"),
    )

TOE_KICK_DEPTH_CHOICES = (
    (0, "Select Depth"),
    (10.50, "10.5''"),
    (14.50, "14.5''"),
    (22.50, "22.5''"),
)

class ShelfTypeChoices(object):

  
    SHELF_TYPE_CHOICES = (
        (1, "Adj."),
        (2, "KD"),
    )
    def get_adj_id(self):
        return 1

    
class ShelfPartitionChoices(object):

      SHELF_PARTITION_CHOICES = (
        (1, "Sq"),
        
    )


EXPOSED_END_CHOICES = (
        ("none", "None"),
        ("single", "Single Exposed Ends"),
        ("both", "Both Exposed Ends"),
        
    )

class DrawerHole(object):

    HOLE_CHOICES = (
        ('3 Hole (3.62")', '3 Hole (3.62")'),
        ('4 Hole (4.88")', '4 Hole (4.88")'),
        ('5 Hole (6.14")', '5 Hole (6.14")'),
        ('6 Hole (7.40")', '6 Hole (7.40")'),
        ('7 Hole (8.66")', '7 Hole (8.66")'),
        ('8 Hole (9.92")', '8 Hole (9.92")'),
        ('9 Hole (11.18")', '9 Hole (11.18")'),
        ('10 Hole (12.44")', '10 Hole (12.44")'),                   
    )
class DrawerWidth(object):

    DWRAWER_WIDTH_CHOICES = (
        (15.58, '15.58'),
        (18.58, '18.58'),
        (21.58, '21.58'),
        (24.58, '24.58'),
        (27.58, '27.58'),                   
        (30.58, '30.58'),
        
    )

class DrawerDrilSubFront(object):
    DRILL_SUB_FRONT_CHOICES=(
        ('No Drill','No Drill'),
        ('pull 76 mm','pull 76 mm'),
        ('pull 96 mm','pull 96 mm'),
        ('pull 128 mm','pull 128 mm'),
        ('Knob','Knob'),
        ('Custom','Custom'),
    )
class DrawerhamperTypes(object):
    HAMPER_FACES_TYPES=(
        ('18H (22.52)','18H (22.52)'),
        ('19H (23.78)','19H (23.78)'),
       
    )

#  PARTITION = "Partition"
#     KD_SHELF = "KD Shelf"
#     IN_KD_SHELF = "1in KD Shelf"
#     SINGLE_DOOR = "Door (Single)"
#     PAIR_DOOR = "Pair Doors"
#     ADJ_SHELF = "Adj Shelf"
#     IN_ADJ_SHELF = "1in Adj Shelf"
#     SHOE_SHELF = "Show Shelf"
#     DRAWER_BOX = "Drawer Box"
#     CUSTOM_SHELF = 'Custom Shelf'
#     CLEAT = 'Cleats'
#     TOE_KICK = 'Toe Kick'
#     l_SHELF='L-SHELF'
#     CORNER_SHELF='CORNER-SHELF'
#     TOP_SHELF='TOP_SHELF'
#     DRAWER_FACES='DRAWER FACES'
class UrlMap(Description):
    ''' For redirect to respective edit page form order details page, wherenever url change need to update this config'''
    def url_map(self):
        url_config={
            self.PARTITION:'/classy/room/room_partition/{0}/edit/{1}',
            self.KD_SHELF:'/classy/room/room_kd_shelf/',
            self.SINGLE_DOOR:"/classy/room/single_door/{0}/?room_item={1}",            
            self.PAIR_DOOR:"/classy/room/pair_doors/{0}/?room_item={1}",
            self.DRAWER_BOX:"/classy/room/drawer_box/{0}/edit/{1}",
            self.CLEAT :"/classy/room/cleat/{0}/edit/{1}",
            self.TOE_KICK:"/classy/room/toe-kicks/{0}/edit/{1}",    
            self.l_SHELF:"/classy/room/l-shelf/{0}/?room_item={1}",
            self.CORNER_SHELF:"/classy/room/corner-shelf/{0}/?room_item={1}",
            self.TOP_SHELF:"/classy/room/top-shelf/{0}?type={2}&room_item={1}",
            self.DRAWER_FACES:"/classy/room/drawer-faces/{0}?type={2}&room_item={1}",
        }

        return url_config
        