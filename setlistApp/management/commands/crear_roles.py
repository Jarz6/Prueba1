from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Crea los 3 grupos requeridos y usuarios de prueba'

    def handle(self, *args, **kwargs):
        roles = ['Administrador', 'Supervisor', 'Administrativo']
        for rol in roles:
            grupo, created = Group.objects.get_or_create(name=rol)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo creado: {rol}'))

        # Usuarios de prueba: admin_user, super_user, adminis_user
        cuentas = [
            ('admin_user', 'admin1234', 'Administrador'),
            ('super_user', 'super1234', 'Supervisor'),
            ('adminis_user', 'adminis1234', 'Administrativo'),
        ]

        for username, password, rol in cuentas:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password, email=f"{username}@inacap.cl")
                grupo = Group.objects.get(name=rol)
                user.groups.add(grupo)
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado con rol {rol}'))
            else:
                self.stdout.write(f'Usuario {username} ya existe')