# Generated by Django 2.2.12 on 2021-02-23 23:46

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0054_remove_home_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='appliances',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('DISH', 'Dishwasher'), ('GARB', 'Garbage disposal'), ('OVEN', 'Oven'), ('REFRIG', 'Refrigerator'), ('NON', 'None')], default=None, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='basement',
            field=models.CharField(blank=True, choices=[('FINI', 'Finished'), ('UNFI', 'Unfinished'), ('PART', 'Partially finished'), ('NON', 'None')], default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='building_amenities',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('BASK', 'Basketball court'), ('CONT', 'Controlled access'), ('DISA', 'Disabled access'), ('DOOR', 'Doorman'), ('ELEV', 'Elevator'), ('FITN', 'Fitness Center'), ('GATE', 'Gated entry'), ('NEAR', 'Near Transportation'), ('SPOR', 'Sports court')], default=None, max_length=44, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='cooling_type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CENT', 'Central'), ('EVAP', 'Evaporative'), ('GEOT', 'Geothermal'), ('REFR', 'Refrigeration'), ('SOLA', 'Solar'), ('WALL', 'Wall'), ('OTHE', 'Other'), ('NON', 'None')], default=None, max_length=38, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='deal_closed',
            field=models.CharField(choices=[('YES', 'yes'), ('NO', 'No')], default='NO', max_length=3),
        ),
        migrations.AlterField(
            model_name='home',
            name='exterior',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('BRIC', 'Brick'), ('CE/CO', 'Cement/Concrete'), ('STON', 'Stone'), ('VINY', 'Vinyl'), ('WOOD', 'Wood'), ('OTH', 'Other')], default=None, max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='floor_covering',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CARP', 'Carpet'), ('CONC', 'Concrete'), ('HARD', 'Hardwood'), ('TILE', 'Tile'), ('SOFT', 'SoftWood'), ('OTH', 'Other')], default=None, max_length=28, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='floor_number',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='garage_sqm',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='heating_fuel',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('COAL', 'Coal'), ('ELEC', 'Electric'), ('GAS', 'Gas'), ('OIL', 'Oil'), ('PR/BU', 'Propane/Butane'), ('SOLA', 'Solar'), ('WO/PE', 'Wood/Pelet'), ('OTH', 'Other'), ('NON', 'None')], default=None, max_length=42, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='heating_type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('BASE', 'Baseboard'), ('FORC', 'Forced air'), ('GEOT', 'Geothermal'), ('HEAT', 'Heat pump'), ('RADI', 'Radiant'), ('STOV', 'Stove'), ('WALL', 'Wall'), ('OTH', 'Other')], default=None, max_length=38, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='indoor_features',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ATTI', 'Attic'), ('CEIL', 'Ceiling fans'), ('DOUB', 'Double pane windows'), ('FIRE', 'Fireplace'), ('SECU', 'Security system'), ('SKYL', 'Skylights'), ('VAUL', 'Vaulted ceiling')], default=None, max_length=34, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='number_of_stories',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='outdoor_amenities',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('BALC', 'Balcony'), ('FENC', 'Fenced yard'), ('GARD', 'Garden'), ('GREEN', 'Greenhouse'), ('LAWN', 'Lawn'), ('POND', 'Pond'), ('POOL', 'Pool'), ('SAUN', 'Sauna'), ('SPRI', 'Sprinkler system'), ('wATER', 'Waterfront')], default=None, max_length=51, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='parking',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'), ('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'), ('ONST', 'On-street'), ('NON', 'None')], default=None, max_length=34, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='parking_spaces',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='property_name',
            field=models.CharField(db_index=True, default=None, max_length=120),
        ),
        migrations.AlterField(
            model_name='home',
            name='roof',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ASPH', 'Asphalt'), ('TILE', 'Tile'), ('SLAT', 'Slate'), ('OTH', 'Other')], default=None, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='rooms',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('BREA', 'BreakFast nook'), ('DINI', 'Dining room'), ('FAMI', 'Family room'), ('LIBR', 'Library'), ('MAST', 'Master bath'), ('MUDR', 'Mud room'), ('OF', 'Office'), ('PANT', 'Pantry'), ('RECR', 'Recreation room'), ('WORK', 'Workshop'), ('So/AR', 'Solarium/Atrium'), ('SUNR', 'Sun room'), ('WALK', 'walk-in-closet')], default=None, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='view',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CITY', 'City'), ('TERR', 'Territorial'), ('MOUN', 'Mountain'), ('WATE', 'Water'), ('PARK', 'Park'), ('NON', 'None')], default=None, max_length=28, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='year_built',
            field=models.PositiveIntegerField(default=2000, null=True),
        ),
    ]
