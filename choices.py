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
        ('automatic', 'Automatic'),
    ]

    PAYMENT_STATUS = [
        ('done', 'DONE'),
        ('pending', 'PENDING'), 
        ('failed', 'FAILED')
    ]

    CUSTOMER_SEGMENT_CHOICES = [
        ('self_employee', 'Self Employment'),
        ('professional', 'Professional')
    ]

    APPLICATION_STATUS_CHOICES = [
        ('ro_phase', 'RO Phase'),
        ('do_phase', 'DO phase'),
        ('md_phase', 'MD Phase'),
        ('bm_phase', 'BM phase'),
        ('technical_officer', 'Technical Officer'),
        ('cluster', 'Cluster')
    ]
    
    IS_EXISTING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]