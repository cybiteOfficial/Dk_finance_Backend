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
        ('yes', 'Yes'),
        ('no', 'No')
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
        ('in_progress', 'In progress'),
        ('approved', 'Approved'),
    ]
    
    IS_EXISTING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]