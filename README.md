# OSRS Mass
A django based web application that allows users to create and join mass events in Old School Runescape.

## Installation

.env file should be created in the root directory with the following variables:
```bash
SECRET_KEY=yoursecretkey
ALLOWED_HOSTS=*
DEBUG=True
TIME_ZONE=Europe/Helsinki
```

```bash

## Roadmap

### Website
- [ ] Create mass event
- [ ] Join the event with nickname by invite code
- [ ] Display event details
- [ ] Display event participants

### Authentication

- [ ] User authentication
- [ ] User profile
- [ ] User password reset
- [ ] User email verification


### Mass functionality
- [ ] Create mass event
- [ ] Nickname when joining event
- [ ] Display event details
- [ ] Display event participants
- [ ] Join the event with invite code
- [ ] Join event with a join link


### Scraping data from OSRS wiki

- [ ] Scrape data from OSRS wiki with API(if available) otherwise use beautifulsoup
- [ ] Store data in database
- [ ] Display data on website