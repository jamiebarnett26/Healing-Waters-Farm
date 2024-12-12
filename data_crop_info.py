from database import sqlalchemy, os, dotenv

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()
_engine = sqlalchemy.create_engine(_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=_engine))

class Family (Base):
    __tablename__ = 'family'
    family_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    family_name = sqlalchemy.Column(sqlalchemy.String)

class Species (Base):
    __tablename__ = 'species'
    species_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    family_id = sqlalchemy.Column(sqlalchemy.Integer)
    latin_name = sqlalchemy.Column(sqlalchemy.String)
    species_name = sqlalchemy.Column(sqlalchemy.String)

class Variety (Base):
    __tablename__ = 'variety'
    variety_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    species_id = sqlalchemy.Column(sqlalchemy.Integer)
    variety_name = sqlalchemy.Column(sqlalchemy.String)

class Crop_Info (Base):
    __tablename__ = 'crop_infos'
    crop_info_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    variety_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    crop_type = sqlalchemy.Column(sqlalchemy.String)
    days_to_maturity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    plant_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    plant_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    row_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    row_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_maturity_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_maturity_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_transplantation = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_direct_sow = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_seed_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    frost_sensitivity_rating = sqlalchemy.Column(sqlalchemy.Integer)

#-----------------------------------------------------------------------

_engine = sqlalchemy.create_engine(_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=_engine))

def get_session():
    """Helper function to retrieve a session from the scoped session factory"""
    return Session()

def search_field_name(search_field, search_value):
    results = []
    with get_session() as session:
        if search_field == 'family':
            query = session.query(Family).filter(
                Family.family_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                family = {
                    'family_id':row.family_id,
                    'family_name':row.family_name
            }
                results.append(family)

        if search_field == 'species':
            query = session.query(Species).filter(
                Species.species_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                species = {
                    'species_id':row.species_id,
                    'family_id':row.family_id,
                    'latin_name':row.latin_name,
                    'species_name':row.species_name
            }
                results.append(species)
  
        
        if search_field == 'variety':
            query = session.query(Variety).filter(
                Variety.variety_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                variety = {
                    'variety_id':row.variety_id,
                    'species_id':row.species_id,
                    'variety_name':row.variety_name
            }
                results.append(variety)
    return results

def search_field_id(search_field, search_value):
    results = []
    with get_session() as session:
        if search_field == 'family':
            query = session.query(Family).filter(
                Family.family_id == search_value
            )
            table = query.all()
            for row in table:
                family = {
                    'family_id':row.family_id,
                    'family_name':row.family_name
            }
                results.append(family)

        if search_field == 'species':
            query = session.query(Species).filter(
                Species.species_id == search_value,
            )
            table = query.all()
            for row in table:
                species = {
                    'species_id':row.species_id,
                    'family_id':row.family_id,
                    'latin_name':row.latin_name,
                    'species_name':row.species_name
            }
                results.append(species)
  
        
        if search_field == 'variety':
            query = session.query(Variety).filter(
                Variety.variety_id == search_value,
            )
            table = query.all()
            for row in table:
                variety = {
                    'variety_id':row.variety_id,
                    'species_id':row.species_id,
                    'variety_name':row.variety_name
            }
                results.append(variety)
        
        if search_field == 'crop_info':
            query = session.query(Crop_Info).filter(
                Crop_Info.crop_info_id == search_value,
            )
            table = query.all()
            for row in table:
                crop_info = {
                'crop_info_id': row.crop_info_id,  # Use ':' instead of '='
                'variety_id': row.variety_id,
                'crop_type': row.crop_type,
                'user_id':row.user_id,
                'days_to_maturity': row.days_to_maturity,
                'plant_spacing_harvest': row.plant_spacing_harvest,
                'plant_spacing_seed': row.plant_spacing_seed,
                'row_spacing_harvest': row.row_spacing_harvest,
                'row_spacing_seed': row.row_spacing_seed, 
                'days_to_maturity_harvest': row.days_to_maturity_harvest,
                'days_to_maturity_seed': row.days_to_maturity_seed,
                'days_to_transplantation': row.days_to_transplantation,
                'days_to_direct_sow': row.days_to_direct_sow,
                'days_to_harvest': row.days_to_harvest,
                'days_to_seed_harvest': row.days_to_seed_harvest,
                'frost_sensitivity_rating': row.frost_sensitivity_rating
            }
                results.append(crop_info)

    return results

def species_from_family(family_id):
    species = []
    with get_session() as session:
        query = session.query(Species).filter(
            Species.family_id == family_id
        )
        table = query.all()
        for row in table:
            spec = {
                'species_id': row.species_id,
                'family_id': family_id,
                'latin_name': row.latin_name,
                'species_name': row.species_name
            }
            species.append(spec)
    return species

def variety_from_species(species_id):
    varieties = []
    with get_session() as session:
        query = session.query(Variety).filter(
            Variety.species_id == species_id
        )
        table = query.all()
        for row in table:
            variety = {
                'variety_id': row.variety_id,
                'species_id': species_id,
                'variety_name': row.variety_name
            }
            varieties.append(variety)
    return varieties

def crop_info_from_variety(variety_id):
    crop_infos = []
    with get_session() as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.variety_id == variety_id
        )
        
        table = query.all()
        for row in table:
            crop_info = {
                'crop_info_id': row.crop_info_id,  # Use ':' instead of '='
                'variety_id': variety_id,
                'crop_type': row.crop_type,
                'user_id':row.user_id,
                'days_to_maturity': row.days_to_maturity,
                'plant_spacing_harvest': row.plant_spacing_harvest,
                'plant_spacing_seed': row.plant_spacing_seed,
                'row_spacing_harvest': row.row_spacing_harvest,
                'row_spacing_seed': row.row_spacing_seed, 
                'days_to_maturity_harvest': row.days_to_maturity_harvest,
                'days_to_maturity_seed': row.days_to_maturity_seed,
                'days_to_transplantation': row.days_to_transplantation,
                'days_to_direct_sow': row.days_to_direct_sow,
                'days_to_harvest': row.days_to_harvest,
                'days_to_seed_harvest': row.days_to_seed_harvest,
                'frost_sensitivity_rating': row.frost_sensitivity_rating
            }

            crop_infos.append(crop_info)
    return crop_infos

def family_from_species(species_id):
    with get_session() as session:
        query = session.query(Species).filter(
            Species.species_id == species_id
        )
        species_table = query.first()
        query = session.query(Family).filter(
            Family.family_id == species_table.family_id
        )
        family_table = query.first()
        return family_table

def species_from_variety(variety_id):
    with get_session() as session:
        query = session.query(Variety).filter(
            Variety.variety_id == variety_id
        )
        variety_table = query.first()
        query = session.query(Species).filter(
            Species.species_id == variety_table.species_id
        )
        species_table = query.first()
        return species_table


def full_crop_info(crop_info_id):
    with get_session() as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.crop_info_id == crop_info_id
        )
        info_table = query.first()
        if not info_table:
            return None  # Ensure you handle None to avoid AttributeError

        query = session.query(Variety).filter(
            Variety.variety_id == info_table.variety_id
        )
        variety_table = query.first()
        if not variety_table:
            return None  # Similarly, handle None for variety_table

        species_table = species_from_variety(info_table.variety_id)
        if not species_table:
            return None  # Check for None before proceeding to avoid crashes

        family_table = family_from_species(species_table.species_id)
        if not family_table:
            return None

        crop_info = {
            'variety_id': variety_table.variety_id,  # Include variety_id explicitly
            'family_name': family_table.family_name,
            'latin_name': species_table.latin_name,
            'user_id':info_table.user_id,
            'species_name': species_table.species_name,
            'species_id': species_table.species_id,
            'variety_name': variety_table.variety_name,
            'crop_type': info_table.crop_type,
            'days_to_maturity': info_table.days_to_maturity,
            'plant_spacing_harvest': info_table.plant_spacing_harvest,
            'plant_spacing_seed': info_table.plant_spacing_seed,
            'row_spacing_harvest': info_table.row_spacing_harvest,
            'row_spacing_seed': info_table.row_spacing_seed,
            'days_to_maturity_harvest': info_table.days_to_maturity_harvest,
            'days_to_maturity_seed': info_table.days_to_maturity_seed,
            'days_to_transplantation': info_table.days_to_transplantation,
            'days_to_direct_sow': info_table.days_to_direct_sow,
            'days_to_harvest': info_table.days_to_harvest,
            'days_to_seed_harvest': info_table.days_to_seed_harvest,
            'frost_sensitivity_rating': info_table.frost_sensitivity_rating
        }
        return crop_info

def add_family(family):
    with get_session() as session:
        new_family = Family(**family)
        session.add(new_family)
        session.commit()

def add_species(species):
     with get_session() as session:
        new_species = Species(**species)
        session.add(new_species)
        session.commit()

def add_variety(variety, crop_info):
    crop_info = {key: (None if value == 'None' else value) for key, value in crop_info.items()}
    with get_session() as session:
        new_variety = Variety(**variety)
        session.add(new_variety)
        session.commit()

        crop_info['variety_id'] = new_variety.variety_id

        new_crop_info = Crop_Info(**crop_info)
        session.add(new_crop_info)
        session.commit()

def edit_family(family_id, updated_data):
    with get_session() as session:
        family = session.query(Family).get(family_id)
        if family:
            for key, value in updated_data.items():
                setattr(family, key, value)
            session.commit()

def edit_species(species_id, updated_data):
    with get_session() as session:
        species = session.query(Species).get(species_id)
        if species:
            for key, value in updated_data.items():
                setattr(species, key, value)
            session.commit()

def edit_variety(variety_id, updated_data_variety, updated_data_crop):
    # Clean up "None" and empty string values
    updated_data_crop = {key: value if value not in ["None", ""] else None for key, value in updated_data_crop.items()}
    updated_data_variety = {key: value if value not in ["None", ""] else None for key, value in updated_data_variety.items()}
    
    with get_session() as session:
        try:
            # Update Crop_Info
            crop_info = session.query(Crop_Info).get(variety_id)
            if crop_info:
                for key, value in updated_data_crop.items():
                    setattr(crop_info, key, value)

            # Update Variety
            variety = session.query(Variety).get(variety_id)
            if variety:
                # Validate non-null fields
                if "variety_name" in updated_data_variety and updated_data_variety["variety_name"] is None:
                    raise ValueError("variety_name cannot be null")
                for key, value in updated_data_variety.items():
                    setattr(variety, key, value)

            # Commit changes
            session.commit()

        except Exception as e:
            session.rollback()  # Rollback in case of any error
            raise e  # Re-raise the exception for debugging
        
def delete_family(family_id):
    with get_session() as session:
        family_to_delete = session.query(Family).filter_by(family_id=family_id).first()

        species = species_from_family(family_id)
        for spec in species:
            delete_species(spec['species_id'])

        session.delete(family_to_delete)
        session.commit()

def delete_species(species_id):
    with get_session() as session:
        species_to_delete = session.query(Species).filter_by(species_id=species_id).first()

        varieties = variety_from_species(species_id)
        for variety in varieties:
            delete_variety(variety['variety_id'])

        session.delete(species_to_delete)
        session.commit()
    
def delete_variety(variety_id):
    with get_session() as session:
        variety_to_delete = session.query(Variety).filter_by(variety_id=variety_id).first()

        crop_infos = crop_info_from_variety(variety_id)
        for crop_info in crop_infos:
            crop_info_to_delete = session.query(Crop_Info).filter_by(crop_info_id=crop_info['crop_info_id']).first()
            session.delete(crop_info_to_delete)
            session.commit()

        session.delete(variety_to_delete)
        session.commit()