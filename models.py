from django.db import models
from markdown import markdown
from tagging.fields import TagField


# Create your models here.

class GovAbstract(models.Model):
    """
    An abstract base class covering basic metadata, 
    including name, slug, description, description_html, url
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True, editable=False)
    url = models.URLField(blank=True)


    class Meta:
        abstract = True
        ordering = ['name']


    def __unicode__(self):
        return self.name



class Branch(GovAbstract):
    """
    A branch of the federal government: Legislative, Executive, Judicial
    """

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Branches"


    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(Branch, self).save()



class Agency(GovAbstract):
    """
    A federal government agency, which is part of a branch.

   For example, the House of Representatives is an agency of the Legislative Branch, while the FDA is part of the Executive Branch.
    """
    branch = models.ForeignKey(Branch)
    

    class Meta:
        ordering = ['branch', 'name']
        verbose_name_plural = "Agencies"


    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(Agency, self).save()
    
    
    @models.permalink
    def get_absolute_url(self):
        return ("fedblogger_agency_detail", (), {'agency_id': self.slug})


class AuthorType(models.Model):
    """
    Some blogs here are going to be 'official' agency blogs,
    while others might just be those written by staff, or by directors.

    This model helps sort by authority.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


    class Meta:
        ordering = ['name']


    def __unicode__(self):
        return self.name



class BlogFeed(GovAbstract):
    """
    A blog by a federal agency or employee thereof, plus the feed url
    """
    PENDING = 1
    APPROVED = 2
    DEFUNCT = 3
    FEED_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DEFUNCT, 'Defunct'),
    )
    agency = models.ForeignKey(Agency)
    author_type = models.ForeignKey(AuthorType)
    feed_url = models.URLField()
    status = models.IntegerField(choices=FEED_STATUS_CHOICES, default=PENDING)
    topics = TagField()
    updated = models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['agency', 'name']


    def __unicode__(self):
        return self.name
    
    
    @models.permalink
    def get_absolute_url(self):
        return ("fedblogger_blog_detail", (), {'agency_id': self.agency.slug, 'blog_id': self.slug})
    
    
    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(BlogFeed, self).save()


    def get_updated(self):
        try:
            self.updated = self.entries.all()[0].pub_date
            self.save()
        except IndexError: # no entries yet
            pass


class BlogEntry(models.Model):
    """
    An actual blog entry, pulled from a BlogFeed's xml feed.
    """
    blog = models.ForeignKey(BlogFeed, related_name="entries")
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    text = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    guid = models.CharField(max_length=255, unique=True, db_index=True)


    class Meta:
        get_latest_by = "pub_date"
        ordering = ['-pub_date']
        verbose_name_plural = "Blog Entries"


    def __unicode__(self):
        return self.title

    
    def get_absolute_url(sefl):
        return self.link
