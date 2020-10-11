from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.

SEX_CHOICES = (
	('M', 'Male'), 
	('F', 'Female')
)

class MarriageManager(models.Manager):
    def marriage_with(self, family_member):
        marriages = self.all()
        marriages = marriages.filter(\
        					Q(descendant=family_member.id) | \
        					Q(in_law=family_member.id))
        return marriages

    def marriage_of(self, family_member1, family_member2):
        marriages = self.all()
        marriages = marriages.filter(\
        						Q(descendant=family_member1.id) | \
        						Q(in_law=family_member1.id))

        marriages = marriages.filter(\
        						Q(descendant=family_member2.id) | \
        						Q(in_law=family_member2.id))
        
        if len(marriages) != 1:
            return None
        else:
            return marriages[0]

class Marriage(models.Model):
    descendant = models.ForeignKey('FamilyMember', models.DO_NOTHING, 
    												related_name='descendant')
    in_law = models.ForeignKey('FamilyMember', models.DO_NOTHING, 
    													related_name='in_law')

    date_of_marriage = models.DateField(null=True, blank=True)
    is_divorced = models.BooleanField()

    objects = MarriageManager()

    def _get_descendant_children_id_list(self):
        descendant_children = self.descendant.children.all()
        children_ids = list()
        for child in descendant_children :
            children_ids.append(child.pk)
        return children_ids

    def get_children(self):
        children_ids = self._get_descendant_children_id_list()
        return self.in_law.children.all().filter(pk__in=children_ids).order_by('date_of_birth')

    def get_step_children(self):
        children_ids = self._get_descendant_children_id_list()
        return self.in_law.children.all().exclude(pk__in=children_ids).order_by('date_of_birth')


    @property
    def marriage_title(self):
        return f'{self.descendant.full_name} & {self.in_law.full_name}'

    def __str__(self):
        return self.marriage_title

class FamilyMemberManager(models.Manager):
    def search_members(self, first=None, middle=None, last=None, maiden=None):
        querySet = self.all()
        if last:
            querySet = querySet.filter(last_name__icontains=last)
        if first:
            querySet = querySet.filter(first_name__icontains=first)
        if middle:
            querySet = querySet.filter(middle_name__icontains=middle)
        if maiden:
            querySet = querySet.filter(maiden_name__icontains=maiden)
        return querySet

    def find_exact_members(self, first=None, middle=None, last=None, maiden=None):
        querySet = self.all()
        if last:
            querySet = querySet.filter(last_name__iexact=last)
        if first:
            querySet = querySet.filter(first_name__iexact=first)
        if middle:
            querySet = querySet.filter(middle_name__iexact=middle)
        if maiden:
            querySet = querySet.filter(maiden_name__iexact=maiden)
        return querySet        

    def find_person(self, first=None, middle=None, last=None, maiden=None):
        if first == '':
            first = None
        if middle == '':
            middle = None
        if last == '':
            last = None
        if maiden == '':
            maiden = None
        firstTry = self.search_members(first, middle, last, maiden)
        if len(firstTry) != 1:
            secondTry = self.find_exact_members(first, middle, last, maiden)
            if len(secondTry) != 1:
                return None
            return secondTry[0]
        return firstTry[0]

class FamilyMember(models.Model):
    #Name
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    maiden_name = models.CharField(max_length=50, blank=True)

    #Personal Info
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    is_step_child = models.BooleanField()

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    #Relationships
    parents = models.ManyToManyField('self', null=True, blank=True, 
    								related_name='ps', symmetrical=False)    
    children = models.ManyToManyField('self', null=True, blank=True, 
									related_name='cs', symmetrical=False)

    #Manager Objects
    objects = FamilyMemberManager()


    def get_children(self):
        children_ids = self._get_descendant_children_id_list()
        return self.in_law.children.all().filter(pk__in=children_ids).order_by('date_of_birth')

    @property
    def full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    @property
    def parents_marriage(self):
        parents = self.parents.all()

        if len(parents) == 2:
            parents_marriage = Marriage.objects.marriage_of(parents[0],parents[1])
        else:
            parents_marriage = None

        return parents_marriage

    class Meta:
        ordering = ('first_name','last_name')
        verbose_name = "Family Member"
        verbose_name_plural = "Family Members" 

    
    def __str__(self):
        return self.full_name


@receiver(post_save, sender=FamilyMember)
def add_parent(sender, instance, **kwargs):
	print("ADDING PARENT")
	for parent in instance.parents.all():
		try:
			me = parent.children.get(id=instance.pk)
		except:
			parent.children.add(instance)


@receiver(post_save, sender=FamilyMember)
def add_children(sender, instance, **kwargs):
	print("ADDING CHILD")
	for child in instance.children.all():
		try:
			me = child.parents.get(id=instance.pk)
		except Exception as e:
			child.parents.add(instance)