from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey
from django.core.urlresolvers import reverse

"""Variables used by pages throughout the site"""
class GlobalVars(models.Model):
    variable = models.CharField(max_length = 200)
    val = models.TextField()
    human_title = models.CharField(max_length = 200)
	
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'
    
    def __unicode__(self):
        return self.human_title + " = " + self.val
        
"""Featured images for home page"""
# consider removing
class FeaturedImgs(models.Model):
    uri = models.URLField()
    description = models.CharField(max_length = 200)

    class Meta:
        verbose_name = 'Featured Image'
        verbose_name_plural = 'Featured Images'
        
    def __unicode__(self):
        return self.description
    
"""Types of Media, such as image/jpeg, text/html, etc"""
# consider removing
class MediaType(models.Model):
    type = models.CharField(max_length = 40)

    def __unicode__(self):
        return self.type
        
"""Used to be more specific about an object type, such as location (type of subject)"""
class ObjectType(models.Model):
    type = models.CharField(max_length = 40)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User) 
    control_field = models.BooleanField(default = False)    

    def __unicode__(self):
        return self.type 

"""Types of descriptive properties (or variables to describe objects)"""
class DescriptiveProperty(models.Model):
    SUBJECT_OBJECT = 'SO'
    SUBJECT_LOC = 'SL'
    MEDIA_PUB = 'MP'
    MEDIA_FILE = 'MF'
    PERSON_ORGANIZATION = 'PO'
    ALL = 'AL'
    TYPE = (
        (SUBJECT_OBJECT, 'Object'),
        (SUBJECT_LOC, 'Location'),
        (MEDIA_PUB, 'Publication'),
        (MEDIA_FILE, 'File'),
        (PERSON_ORGANIZATION, 'Person/Organization'),
        (ALL, 'All'),
    )
    
    INT = '_i'
    STRING = '_s'
    LONG = '_l'
    TEXT = '_t'
    BOOLEAN = '_b'
    FLOAT = '_f'
    DOUBLE = '_d'
    DATE = '_dt'
    LOCATION = '_p'
    SOLR_TYPE = (
        (INT, 'Integer'),
        (STRING, 'String'),
        (LONG, 'Long'),
        (TEXT, 'Text'),
        (BOOLEAN, 'Boolean'),
        (FLOAT, 'Float'),
        (DOUBLE, 'Double'),
        (DATE, 'Date'),
        (LOCATION, 'Location'),
    )
    
    GEN = 'gen'
    CON = 'con'
    ARCH = 'arc'
    TEXT = 'txt'
    DATA_SOURCE_TYPE = (
        (GEN, 'General'),
        (CON, 'Conservation-Analytic'),
        (ARCH, 'Archival'),
        (TEXT, 'Textual'),
    )

    property = models.CharField(max_length = 60)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    primary_type = models.CharField(max_length=2, choices=TYPE, default=ALL, blank = True)
    order = models.IntegerField(blank = True, default=99)
    visible = models.BooleanField(default = False)
    solr_type = models.CharField(max_length = 45, choices = SOLR_TYPE, default = TEXT, blank = True)
    facet = models.BooleanField(default = False)
    control_field = models.BooleanField(default = False)
    data_source_type = models.CharField(max_length=3, choices=DATA_SOURCE_TYPE, default = GEN, blank = True)

    def __unicode__(self):
        return self.property
        
    class Meta:
        verbose_name = 'Descriptive Property'
        verbose_name_plural = 'Descriptive Properties'
        ordering = ['order']

"""Descriptive properties used for displaying search results"""
class ResultProperty(models.Model):
    display_field = models.CharField(max_length = 40)
    field_type = models.ForeignKey(DescriptiveProperty, blank = True, null = True)
    
    class Meta:
        verbose_name = 'Result Property'
        verbose_name_plural = 'Result Properties'

    def __unicode__(self):
        return self.field_type.property
        
"""Types of relationships between objects"""
class Relations(models.Model):
    relation = models.CharField(max_length = 60)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)    

    def __unicode__(self):
        return self.relation
        
    class Meta:
        verbose_name_plural = 'relations'
        
"""Files that help make up documentation for project"""        
class Media(models.Model):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    type = models.ForeignKey(MediaType, blank = True, null = True)

    class Meta:
        verbose_name_plural = 'media'
    
    def __unicode__(self):
        return self.title
        
    def get_properties(self):
        return self.mediaproperty_set.all()
        
    def get_type(self):
        return 'media';

"""Descriptive Properties of Media Files"""        
class MediaProperty(models.Model):
    media = models.ForeignKey(Media)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)   

    def __unicode__(self):
        return self.property_value
        
    def get_properties(self):
        return self.media.get_properties()

    class Meta:
        verbose_name = 'Media Property'
        verbose_name_plural = 'Media Properties'
        
"""Primary subjects of observation for a project, usually objects or locations"""        
class Subject(models.Model):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)
    type = models.ForeignKey(ObjectType, blank = True, null = True)
    title1 = models.TextField(blank = True)
    title2 = models.TextField(blank = True)
    title3 = models.TextField(blank = True)
    desc1 = models.TextField(blank = True)
    desc2 = models.TextField(blank = True)
    desc3 = models.TextField(blank = True)    
    
    def __unicode__(self):
        return self.title
        
    def get_properties(self):
        return self.subjectproperty_set.all()
        
    def get_type(self):
        return 'subject';
        
    def admin_column(self, column):
        field = ResultProperty.objects.get(display_field = column)
        
        id_str = ''
        
        ids = self.subjectproperty_set.filter(property=field.field_type_id)
        if ids:
            for i, id in enumerate(ids):
                if i > 0:
                    id_str += ', '
                id_str += id.property_value
        return id_str     
        
    def admin_column_name(column):
        field = ResultProperty.objects.get(display_field = column)
        if field:
            return field.field_type
        return ''
    
    def id1(self):
        vals = self.admin_column('subj_title1')
        if vals == '':
            return '(none)'
        return vals
    id1.short_description = admin_column_name('subj_title1')
    def id2(self):
        return self.admin_column('subj_title2')
    id2.short_description = admin_column_name('subj_title2')
    def id3(self):
        return self.admin_column('subj_title3')
    id3.short_description = admin_column_name('subj_title3')
    
    def identifiers(self):
        field1 = ResultProperty.objects.get(display_field = 'subj_title1')
        field2 = ResultProperty.objects.get(display_field = 'subj_title2')
        field3 = ResultProperty.objects.get(display_field = 'subj_title3')

        id_str = ''
        
        ids = self.subjectproperty_set.filter(Q(property=field1.field_type_id) | Q(property=field2.field_type_id) | Q(property=field3.field_type_id))
        for i, id in enumerate(ids):
            if i > 0:
                id_str += ', '
            id_str += id.property_value
        return id_str

    def descriptors(self):
        field1 = ResultProperty.objects.get(display_field = 'subj_desc1')

        desc_str = ''
        
        descs = self.subjectproperty_set.filter(property=field1.field_type_id)
        for i, desc in enumerate(descs):
            if i > 0:
                desc_str += '; '
            desc_str += desc.property_value
        return desc_str

        
    class Meta:
        verbose_name = 'Object'    
        verbose_name_plural = 'Objects' 
        
"""Descriptive Properties of Subjects"""        
class SubjectProperty(models.Model):
    subject = models.ForeignKey(Subject)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    class Meta:
        verbose_name = 'Object Property'    
        verbose_name_plural = 'Object Properties'
        ordering = ['property__order']

    def __unicode__(self):
        return self.property_value
        
    def get_properties(self):
        return self.subject.get_properties()
                
"""The people and institutions that participated in a project"""        
class PersonOrg(models.Model):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    
    class Meta:
        verbose_name = 'Person/Organization'
        verbose_name_plural = 'People/Organizations'    
    
    def __unicode__(self):
        return self.title
        
    def get_properties(self):
        return self.personorgproperty_set.all()
       
    def get_type(self):
        return 'person_org';       

"""Descriptive Properties of People and Organizations"""        
class PersonOrgProperty(models.Model):
    person_org = models.ForeignKey(PersonOrg)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)

    class Meta:
        verbose_name = 'PersonOrg Property'
        verbose_name_plural = 'PersonOrg Properties'    

    def __unicode__(self):
        return self.property_value
        
    def get_properties(self):
        return self.person_org.get_properties()
                
"""Related media and subjects"""
class MediaSubjectRelations(models.Model):
    media = models.ForeignKey(Media)
    subject = models.ForeignKey(Subject)
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    def __unicode__(self):
        return self.media.title + ":" + self.subject.title
        
    class Meta:
        verbose_name = 'Media-Object Relation'
        verbose_name_plural = 'Media-Object Relations'
        
"""Related media and people"""
class MediaPersonOrgRelations(models.Model):
    media = models.ForeignKey(Media)
    person_org = models.ForeignKey(PersonOrg)
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.media.title + ":" + self.person_org.title

    class Meta:
        verbose_name = 'Media-Person/Organization Relation'
        verbose_name_plural = 'Media-Person/Organization Relations'        
        
"""Related subjects"""
class SubjectSubjectRelations(models.Model):
    subject1 = models.ForeignKey(Subject, related_name='subject1')
    subject2 = models.ForeignKey(Subject, related_name='subject2')
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.subject1.title + ":" + self.subject2.title 
        
    class Meta:
        verbose_name = 'Object-Object Relation'
        verbose_name_plural = 'Object-Object Relations'    
        
"""Related media"""
class MediaMediaRelations(models.Model):
    media1 = models.ForeignKey(Media, related_name='media1')
    media2 = models.ForeignKey(Media, related_name='media2')
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.media1.title + ":" + self.media2.title

"""Related persons and organizations"""
class PersonOrgPersonOrgRelations(models.Model):
    person_org1 = models.ForeignKey(PersonOrg, related_name='person_org1')
    person_org2 = models.ForeignKey(PersonOrg, related_name='person_org2')
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.person_org1.title + ":" + self.person_org2.title 
        
"""Object Status"""
class Status(models.Model):
    status = models.CharField(max_length = 60, blank = True)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    def __unicode__(self):
        return self.status 
    
    class Meta:
        verbose_name = 'Status'    
        verbose_name_plural = 'Status'
        
class ControlField(MPTTModel):
    title = models.CharField(max_length = 60, blank = True)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)
    type = models.ForeignKey(DescriptiveProperty, blank = True, null = True)
    parent = TreeForeignKey('self', null = True, blank = True, related_name = 'children')
    
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def __unicode__(self):
        return self.title
        
class LinkedDataSource(models.Model):
    title = models.CharField(max_length = 60, blank = True)
    link = models.URLField(blank = True)

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Linked Data Source'
        verbose_name_plural = 'Linked Data Sources'        

class ControlFieldLinkedData(models.Model):
    control_field = models.ForeignKey(ControlField)
    source = models.ForeignKey(LinkedDataSource)
    link = models.URLField(blank = True)
    
    class Meta:
        verbose_name = 'Linked Data'
        verbose_name_plural = 'Linked Data'
        
class DescPropertyLinkedData(models.Model):
    desc_prop = models.ForeignKey(DescriptiveProperty)
    source = models.ForeignKey(LinkedDataSource)
    link = models.URLField(blank = True)
    
    class Meta:
        verbose_name = 'Linked Data'
        verbose_name_plural = 'Linked Data'        

class SubjectLinkedData(models.Model):
    subject = models.ForeignKey(Subject)
    source = models.ForeignKey(LinkedDataSource)
    link = models.URLField(blank = True)
    
    class Meta:
        verbose_name = 'Linked Object Data'
        verbose_name_plural = 'Linked Object Data'        
        
class SubjectControlProperty(models.Model):
    subject = models.ForeignKey(Subject)
    control_property = models.ForeignKey(DescriptiveProperty)
    control_property_value = models.ForeignKey(ControlField)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    class Meta:
        verbose_name = 'Controled Object Property'    
        verbose_name_plural = 'Controled Object Properties'    

    def __unicode__(self):
        return self.control_property_value        
    
class ArtifactTypeManager(models.Manager):
    def get_query_set(self):
        return super(ArtifactTypeManager, self).get_query_set().filter(type=19)
        
class ArtifactType(ControlField):
    objects = ArtifactTypeManager()
    
    def __unicode__(self):
        return self.title
        
    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = 19
        super(ArtifactType, self).__init__(*args, **kwargs)
    
    class Meta:
        proxy = True
        verbose_name = 'Artifact Type'
        verbose_name_plural = 'Artifact Types'

class PublicationManager(models.Manager):
    def get_query_set(self):
        return super(PublicationManager, self).get_query_set().filter(relation_type=2)
        
class Publication(MediaSubjectRelations):
    objects = PublicationManager()
    
    class Meta:
        proxy = True
        
class FileManager(models.Manager):
    def get_query_set(self):
        return super(FileManager, self).get_query_set().filter(Q(relation_type=3) | Q(relation_type=1))
        
class File(MediaSubjectRelations):
    objects = FileManager()
    
    def get_thumbnail(self):
        rs_ids = MediaProperty.objects.filter(media = self.media_id, property__property = 'Resource Space ID')
        if rs_ids:
            rs_id = rs_ids[0].property_value
            url = 'http://ur.iaas.upenn.edu/resourcespace/plugins/ref_urls/file.php?ref=' + rs_id + '&size=thm'
        else:
            url = 'http://ur.iaas.upenn.edu/static/img/no_img.jpg'
        return u'<img src="%s" />' % url        
    get_thumbnail.short_description = 'Thumbnail'
    get_thumbnail.allow_tags = True
    
    class Meta:
        proxy = True

class Location(MPTTModel):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)
    type = models.ForeignKey(ObjectType, blank = True, null = True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.title
     
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def ancestors(self):
        ancients = self.get_ancestors(include_self=False)
        ancs = ''
        for ancient in ancients:
            ancs = ancs + ancient.title + '>>'
        return ancs
        
class LocationProperty(models.Model):
    location = models.ForeignKey(Location)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    class Meta:
        verbose_name = 'Location Property'    
        verbose_name_plural = 'Location Properties'    

    def __unicode__(self):
        return self.property_value
        
class LocationSubjectRelations(models.Model):
    location = models.ForeignKey(Location)
    subject = models.ForeignKey(Subject)
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    def __unicode__(self):
        return self.location.title + ":" + self.subject.title
        
    class Meta:
        verbose_name = 'Location-Object Relation'
        verbose_name_plural = 'Location-Object Relations'        
        
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User)
        
    class Meta:
        ordering = ['-created']
            
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('base.views.post', args=[self.slug])
        
class MediaLocationRelations(models.Model):
    media = models.ForeignKey(Media)
    location = models.ForeignKey(Location)
    relation_type = models.ForeignKey(Relations)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User, blank = True)

    def __unicode__(self):
        return self.media.title + ":" + self.location.title
        
    class Meta:
        verbose_name = 'Media-Location Relation'
        verbose_name_plural = 'Media-Location Relations'