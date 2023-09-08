# ![image](https://cdn2.iconfinder.com/data/icons/solid-glyphs-volume-1/256/zcaution-128.png) plixa-backend [Experimental]

This is an experimental implementation of plixa-backend that uses FastAPI with MongoDb.
Do not merge into `main` or `dev` branches

## Setup for development

This project request `docker` or `docker-desktop` for development setup

Clone the repository

```bash
git clone https://github.com/saintmalik/plix-backend
```

Change directory to the cloned repository

```bash
cd plix-backend
```

Extract the `.env` file provided into the project's root directory

Spin up a container

```bash
docker compose up --build -d
```

Happy development 😎

## Project Requirements

### End Users

- [x] No auth
- [] Click on make payment
- [] Make a full payment or half payment
- [] In payment dialogue, Enter Full name, phone number, matric number, level, and department/course
- [] Click payment and pay directly to the association account (transfer-based), I suggest mono or kora
- [] Issue a customized receipt (replica of the association receipt) to be downloaded with a QR code for the original
  payment confirmation

### President/Association Lead

- Signup/login to dashboard
    - [] Signup box: Full Name, Matric, School Name, School Short name, Association Name, Association shortened name,
      Level, Constituency name, Department or Faculty option, Session
- Add bank account details
    - [] Enter and verify account name compliance sake, changing it requires submission
    - [] Edition of account number requires checking for bank account number, is it matches that of the local bank and
      does
      the name matches the association name
- Add student's details submitted by students' class governors
    - [] The president/departmental president will see the start session button and select the session they are starting
    - [] The president gets the students' data from the departmental president populated for them
- [] Message/SMS option button to notify students who are yet to pay (proposed for v2)
