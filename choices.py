class Choices:

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    TITLE_CHOICES = [
        ('miss', 'Miss'),
        ('ms.', 'Ms.'),
        ('mrs', 'Mrs.'),
        ('mr.', 'Mr.')
    ]

    USER_TYPE_CHOICES = [
        ("ro", "Ro"), 
        ("do", "Do"), 
        ("technicalofficer", "Technicalofficer"), 
        ("bm", "Bm"),
        ("md", "MD"),
        ("cluster", "Cluster")
    ]

    PRODUCT_TYPE_CHOICES = [
        ('normal', 'Normal'),
    ]
    
    CASE_TAG_CHOICES = [
        ('normal', 'Normal'),
    ]

    CUSTOMER_TYPE_CHOICES = [
        ('home_loan', 'HomeLoan'),
    ]

    SOURCE_TYPE = [
        ('website', 'Website'),
        ('out_source', 'Out_Source')
    ]

    PROOF_TYPE_CHOICES = [
        (),
        ()
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('kyc', 'KYC'),
        ('other', 'Other')
    ]

    VERIFICATION_TYPE_CHOICES = [
        (),
        ()
    ]

    TRANSACTION_TYPE = [
       ('purchase', 'Purchase'),
        ('refinance', 'Refinance'),
        ('construction', 'Construction'),
    ]
    PAYMENT_STATUS = [
        ('Initiated', 'Initiated'),
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
    ]
    
    APPLICATION_STATUS_CHOICES = [
        ('ro_phase', 'Review Phase'),
        ('ap_phase', 'Approval Phase'),
        ('rej_phase', 'Rejection Phase'),
     ]
    CUSTOMER_SEGMENT_CHOICES = [
        ('segment1', 'Segment 1'),
        ('segment2', 'Segment 2'),
        ('segment3', 'Segment 3'),
     ]
    IS_EXISTING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]