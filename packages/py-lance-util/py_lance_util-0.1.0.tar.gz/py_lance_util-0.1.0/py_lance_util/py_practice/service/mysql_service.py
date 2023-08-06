from datetime import datetime
from sqlalchemy.orm import sessionmaker


def generate_data(model, num):
    data_list = []
    for i in range(num):
        entity = model()
        entity.m_id = i
        entity.name = f"lance_{i}"
        entity.identity_no = f"no_{i}"
        entity.address = f"address_{i}"
        data_list.append(entity)
    return data_list


def batch_insert_data(engine: sessionmaker, insert_list):

    t0 = datetime.now()
    engine.bulk_save_objects(insert_list)
    # engine.execute(
    #     entity.__table__.insert(),
    #     insert_list
    # )  # ==> engine.execute('insert into ttable (name) values ("NAME"), ("NAME2")')
    print(
        f"SQLAlchemy Core: Total time for {len(insert_list)} records  {str(datetime.now() - t0)} secs")
