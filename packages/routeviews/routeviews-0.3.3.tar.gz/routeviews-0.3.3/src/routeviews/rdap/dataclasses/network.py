import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Network():
    """UNTESTED: Work in progress.
    """
    email: str
    @classmethod
    def from_data(cls, response) -> 'Network':
        filter(lambda entity: 'technical' in entity['roles'], response['entities'])
        for entity in response['entities']:
            if 'technical' in entity['roles']:
                # rdap has funky vcardArray format.  
                # It looks standardized: hopefully the email_index is consistent
                email_index = 3
                if 'vcardArray' in entity.keys():
                    try:
                        for vcard in entity['vcardArray'][1]:  # TODO, what is at "1" index?
                            if 'email' in vcard:
                                email = vcard[email_index]
                    except IndexError:
                        logger.info('TODO')
        return cls(email=email)