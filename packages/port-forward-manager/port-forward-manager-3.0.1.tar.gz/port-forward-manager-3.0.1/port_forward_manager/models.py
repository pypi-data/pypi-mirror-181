from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import BaseModelDB, engine, SessionLocal

db_session = SessionLocal()


class Group(BaseModelDB):
    name = Column(String, unique=True, nullable=False)
    label = Column(String)
    schemas = relationship('Schema', back_populates='group')

    @staticmethod
    def delete(record: 'Group'):
        db_session.delete(record)
        db_session.commit()

    @staticmethod
    def index(name=None):
        cursor = db_session.query(Group)
        if name:
            search = "%{}%".format(name)
            cursor = cursor.filter(Group.name.like(search))

        return cursor.all()

    @staticmethod
    def find_by(**kwargs):
        cursor = db_session.query(Group)
        return cursor.filter_by(**kwargs).first()

    @staticmethod
    def find_by_id(group_id: int):
        cursor = db_session.query(Group)
        return cursor.filter(Group.id == group_id).first()

    @staticmethod
    def find_by_name(name):
        cursor = db_session.query(Group)
        return cursor.filter(Group.name == name).first()

    @staticmethod
    def add(group: 'Group'):
        db_session.add(group)
        db_session.commit()

    @classmethod
    def query(cls):
        return db_session.query(cls)

    @staticmethod
    def get_state():
        state = []
        for group in Group.index():
            state.append(group.as_dict())

        return state


class Schema(BaseModelDB):
    name = Column(String, unique=True, nullable=False)
    label = Column(String)
    active = Column(Boolean, index=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', back_populates='schemas')
    sessions = relationship('Session', back_populates='schema')

    @staticmethod
    def delete(schema: 'Schema'):
        db_session.delete(schema)
        db_session.commit()

    @staticmethod
    def index(name=None, group_id=None):
        cursor = db_session.query(Schema)
        if name:
            search = "%{}%".format(name)
            cursor = cursor.filter(Schema.name.like(search))

        if group_id:
            cursor = cursor.filter_by(group_id=group_id)

        return cursor.all()

    @staticmethod
    def find_by_name(name):
        cursor = db_session.query(Schema)
        return cursor.filter(Schema.name == name).first()

    @staticmethod
    def find_by_id(schema_id: int):
        cursor = db_session.query(Schema)
        return cursor.filter(Schema.id == schema_id).first()

    def get_session(self, session_type: str, hostname: str, remote_port: int):
        for session in self.sessions:
            # print(session.dict())
            # print(hostname, remote_port)

            if session.hostname == hostname and session.remote_port == remote_port and session_type == session.type:
                # print(session.as_dict())
                return session

        # raise Exception(f"Session {hostname} and {remote_port} not found on {self.id}")

    @staticmethod
    def get_state():
        state = []
        for schema in Schema.index():
            schema_state = schema.as_dict()

            state.append(schema_state)

        return state


class Session(BaseModelDB):
    label = Column(String)
    schema_id = Column(Integer, ForeignKey('schema.id'))
    active = Column(Boolean)
    hostname = Column(String)
    type = Column(String, default='local')
    remote_address = Column(String, default='127.0.0.1')
    remote_port = Column(Integer)
    local_address = Column(String, default='127.0.0.1')
    local_port = Column(Integer)
    local_port_dynamic = Column(Boolean, default=False)
    url_format = Column(String)
    auto_start = Column(Boolean, index=True, default=True)
    schema = relationship('Schema', back_populates='sessions')
    _connected: bool = False

    @staticmethod
    def delete(session: 'Session'):
        db_session.delete(session)
        db_session.commit()

    @staticmethod
    def find_by_id(session_id: int):
        cursor = db_session.query(Session)
        return cursor.filter(Session.id == session_id).first()

    @staticmethod
    def index(hostname=None):
        cursor = db_session.query(Session)
        if hostname:
            search = "%{}%".format(hostname)
            cursor = cursor.filter(Session.hostname.like(search))

        return cursor.all()

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    @property
    def tmux_id(self) -> str:
        fields = [
            'pfm_session',
            '{schema_name}',
            '{hostname}',
            '{remote_address}',
            '{remote_port}',
            '{local_address}',
            '{local_port}',
            '{type}'
        ]

        data = {
            'schema_name': self.schema.name,
            'hostname': self.hostname,
            'remote_address': self.remote_address,
            'remote_port': self.remote_port,
            'local_address': self.local_address,
            'local_port': self.local_port,
            'type': self.type
        }

        return '|'.join(fields).format(**data).replace('.', '_')

    @property
    def url(self):
        if self.url_format and self.connected:
            data = {
                'schema_id': self.schema_id,
                'hostname': self.hostname,
                'remote_address': self.remote_address,
                'remote_port': self.remote_port,
                'local_address': self.local_address,
                'local_port': self.local_port,
                'type': self.type
            }

            return self.url_format.format(**data)
        else:
            return ''

    @property
    def command(self):
        session_data = self.as_dict()

        session_data['tmux_id'] = self.tmux_id
        session_data['shell_command'] = 'ping localhost'

        if self.type == 'remote':
            ssh = 'ssh -o ExitOnForwardFailure=yes -R {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}'
        else:
            ssh = 'ssh -o ExitOnForwardFailure=yes -L {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}'

        session_data['ssh_command'] = ssh.format(**session_data)

        # start_command = "screen -dmS '{name}' {ssh_command}  -- {shell_command}"
        start_command = "tmux new-session -d -s '{tmux_id}' '{ssh_command} -- {shell_command}'".format(**session_data)
        # inspect(session_definition)
        return start_command

    @staticmethod
    def get_state():
        state = []
        for session in Session.index():
            session_state = session.as_dict()
            session_state['connected'] = session.connected
            session_state['url'] = session.url
            state.append(session_state)
        return state


def init_database():
    BaseModelDB.metadata.create_all(engine)


def reset_database():
    BaseModelDB.metadata.drop_all(engine)