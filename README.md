# OSRS Mass

[![Django CI](https://github.com/JonneSaloranta/osrs-mass/actions/workflows/django.yml/badge.svg)](https://github.com/JonneSaloranta/osrs-mass/actions/workflows/django.yml)

A django based web application that allows users to create and join mass events in Old School Runescape.

## Installation

.env file should be created in the root directory with the following variables:

```bash
SECRET_KEY=yoursecretkey
ALLOWED_HOSTS=*
DEBUG=True
TIME_ZONE=Europe/Helsinki
```

## Roadmap

### Website

- [x] Create mass event (admin)
- [x] Display event details
- [ ] Create mass event (user)
- [ ] Join the event with nickname by invite code
- [ ] Display event participants

### Authentication

- [ ] User authentication
- [ ] User profile
- [ ] User password reset
- [ ] User email verification

### Mass functionality

- [x] Create mass event
- [x] Display event details
- [ ] Nickname when joining event
- [ ] Display event participants
- [ ] Join the event with invite code
- [ ] Join event with a join link

### Scraping data from OSRS wiki

- [ ] Scrape data from OSRS wiki with API(if available) otherwise use beautifulsoup
- [ ] Store data in database
- [ ] Display data on website

### MISC

- [x] Add support for .env file
- [x] Add support separeate databases for models
- [ ] Add tests
- [ ] Add CI/CD
- [ ] Add Docker support
- [ ] Add caching
- [ ] Add rate limiting
- [ ] Add Kubernetes support
