from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# mise en place de la classe personaliser pour gerer nos utilisateurs qui etant de la classe BaseUsermanagement parceque je veux personaliser mon modele unser sinon j'aurais pus utiliser modele user personaliser
class CustomUserManager(BaseUserManager):
    # definition de la methode create_user pour creer un utilisateur
    def create_user(self,username,email,password=None,role='user'):
        if not username:
            raise ValueError('user must have an username')
        if not email:
            raise ValueError('user must have an email')
        # normalisation de l'email fournie pas l'utilisateur 
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,role=role)
        # mise a jour du mot de passe user
        user.set_password(password)
        user.save(using=self._db)
        return user
    # definition de la methode create_superuser pour creer un super utilisateur
    def create_superuser(self , username,email,password=None):
        user=self.create_user(username=username,email=email,password=password,role='admin')
        user.is_admin=True
        user.save(using=self._db)
        return user
    # definition de la classe CustomUser qui etant de la classe AbstractBaseUser materialisant les utilisateurs de notre application
class CustomUser(AbstractBaseUser):
    # le champ password n'existe pas parceque je vais utiliser celle de la classe que mon modle herite et a des outils integrer pour gerer les mot de passe fournis par django
    username=models.CharField( unique=True,max_length=100)
    email=models.EmailField(unique=True)
    role=models.CharField(default='user',max_length=100)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    # gestionnaire d'objet pour mon modele CustomUser
    objects=CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
# Create your models here.
# creation du modele pour les taches
class Task(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    # creation du champ qui met un lien entre les utilisateur qt les taches supprimer et qui definir que pour chaque utilisateur supprimer on supprime les taches qui lui sont lie pour eviter d'avoir des donnee orphelin dans la BD
    author= models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title