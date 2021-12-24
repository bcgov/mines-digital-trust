# Permit Issuer Controller Getting Started Tutorial

This Getting Started Guide is to get someone up and running with the Permit Issuer/Controller for Aries VCR.  If you are new to the Aries VCR Issuer Controller, please refer to [their getting started tutorial](https://github.com/bcgov/aries-vcr-issuer-controller/blob/main/GettingStartedTutorial.md). Here, we will assume that you have gone through that generic getting started and are familiar with the components.  We will discuss running locally in Docker.

## Table of Contents <!-- omit in toc -->

- [Permit Issuer Controller Getting Started Tutorial](#permit-issuer-controller-getting-started-tutorial)
  - [Running on Local Machine](#running-on-local-machine)
  - [VON Network Setup](#von-network-setup)
    - [Local Machine](#local-machine-1)
      - [VON Network](#von-network)
      - [Aries VCR](#aries-vcr)
  - [Step 1: Investigating VON](#step-1-investigating-von)
  - [Step 2: Getting Your VON Issuer/Verifier Agent Running](#step-2-getting-your-von-issuerverifier-agent-running)
    - [Submit Credentials via API](#submit-credentials-via-api)

## Running on Local Machine
To run this guide on your local machine, you must have the following installed:

* Docker (Community Edition is fine)
  * If you do not already have Docker installed, go to [the Docker installation page](https://docs.docker.com/install/#supported-platforms) and click the link for your platform.
* Docker Compose
  * Instructions for installing docker-compose on a variety of platforms can be found [here](https://docs.docker.com/compose/install/).
* git
  * [This link](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/) provides installation instructions for Mac, Linux (including if you are running Linux using VirtualBox) and native Windows (without VirtualBox).
* a bash shell
  * bash is the default shell for Mac and Linux.
  * On Windows, the git-bash version of the bash shell is installed with git and it works well. You **must** use bash to run the guide (PowerShell or Cmd will not work).
* curl
  * An optional step in the guide uses the utility `curl`.
  * curl is included on Mac and Linux.
  * Instructions for installing curl on Windows can be found [here](https://stackoverflow.com/questions/9507353/how-do-i-install-and-use-curl-on-windows).

## VON Network Setup
### Local Machine

On a local machine upon which the prerequisites are setup, we will be installing and starting instances of [von-network](https://github.com/bcgov/von-network), and [Aries VCR](https://github.com/bcgov/aries-vcr).

IMPORTANT: if you have cloned, built and started the Von Network and/or the Aries VCR, you will need to clean up the previous instances and start from scratch.  For the respective cloned directories run ```./manage down``` before building and starting.

#### VON Network

In a shell, run the following commands to start von-network:

```bash
git clone https://github.com/bcgov/von-network
cd von-network
./manage build
./manage start
```

After about 20 seconds or so, go to [http://localhost:9000](http://localhost:9000) in your browser and you should see a web page with the status of your network showing four nodes up and running (blue circles). If you don't get the server up immediately, wait longer and refresh your browser.  If you have a atypical docker and hosts setup, you may have to determine how to navigate to the correct page.

If you want to see the logs for von-network (especially if things aren't working), run from the same folder the command `./manage logs`. When you are done with the logs and you want to get back to the command line, type `Ctrl-c`.

When you are finished with the demo and want to stop the running von-network, run from the same folder the command `./manage stop`.

#### Aries VCR

After von-network has started, go to a second shell and run the following commands to start Aries VCR:

```bash
git clone https://github.com/bcgov/aries-vcr
cd aries-vcr/docker
THEME_PATH=../client/themes THEME=bcgov ./manage build
DEBUG=False THEME=bcgov ./manage start
```

The build step will take a long time to run, so sit back and relax...

Once you have run the `start` step and the logs look good, navigate to [http://localhost:8080](http://localhost:8080) in your browser to get to the Aries VCR home page. Sadly, you won't be able to do much because no credentials have been loaded, but at least everything is running!

When you are finished playing with the instance of Aries VCR, go back to your shell, hit Ctrl-c to get back to the command line prompt and run `./manage stop`. That will stop all of the running containers and clean up the volumes created as part of the Aries VCR instance.

Note that the `DEBUG=False` parameter will tell the vcr-agent to register itself; this is critical if you want to verify credentials.  To check that you have registered the agent, use the swagger interface for connections at [http://localhost:8024](http://localhost:8024/api/doc#/connection/get_connections). For GET /connections, click `Try it out` and then `Execute`, the response should contain results, one of which should have `"alias": "credential-registry-self"`.

If you encounter issues, you can always restart particular containers, like so:

```bash
DEBUG=False THEME=bcgov ./manage restart vcr-api
DEBUG=False THEME=bcgov ./manage restart vcr-agent
```

## Step 1: Investigating VON

If you are new to VON, see the instructions in the respective repos for how to use the running instances of [von-network](https://github.com/bcgov/von-network) and [Aries VCR](https://github.com/bcgov/aries-vcr).

Our goal in this guide is to configure a run our VON issuer/verifier agent so that the credential will be discoverable in the Aries VCR instance.

## Step 2: Getting Your VON Issuer/Verifier Agent Running

In this step, we'll get an instance of our new VON issuer/verifier agent running and issuing credentials.

Use a different shell from the one used to start the other components. After opening the new shell, navigate the root of this repository.

To start your agent, run through these steps:

```
cd docker   # Assumes you were already in the root of this repo
./manage build
./manage start
```

After the last command, you will see a stream of logging commands as the agent starts up. The logging should stabilize with a "Completed sync: indy" entry.

When you need to get back to the command line, you can press `CTRL-c` to stop the stream of log commands. Pressing `CTRL-c` does not stop the containers running, it just stops the log from displaying. If you want to get back to seeing the log, you can run the command `./manage logs` from the `docker` folder.

To verify your agent is running:

* Go to the `issuer/controller URL` ([http://localhost:5000](http://localhost:5000)), where you should see a "404" (not found) error message. That signals the issuer/controller is running, but does not respond to that route.

All good?  Whoohoo!

### Submit Credentials via API

To submit credentials, use Postman (or similar, based on your local configuration) to submit the following to http://localhost:5000/issue-credential

```
[
    {
        "schema": "my-registration.bcgov-mines-permitting",
        "version": "1.0.0",
        "attributes": {
            "corp_num": "ABC12345",
            "registration_date": "2018-01-01",
            "entity_name": "Ima Permit",
            "entity_name_effective": "2018-01-01",
            "entity_status": "ACT",
            "entity_status_effective": "2019-01-01",
            "entity_type": "ABC",
            "registered_jurisdiction": "BC",
            "addressee": "A Person",
            "address_line_1": "123 Some Street",
            "city": "Victoria",
            "country": "Canada",
            "postal_code": "V1V1V1",
            "province": "BC",
            "effective_date": "2019-01-01",
            "expiry_date": ""
        }
    },
    {
        "schema": "bcgov-mines-act-permit.bcgov-mines-permitting",
        "version": "1.0.0",
        "attributes": {
            "permit_id": "MYPERMIT12345",
            "entity_name": "Ima Permit",
            "corp_num": "ABC12345",
            "permit_issued_date": "2018-01-01",
            "permit_type": "ABC",
            "permit_status": "OK",
            "effective_date": "2019-01-01"
        }
    }
]
```

You should get a 200 OK response like:
```
[
    {
        "result": "91b94a05-f0a5-4708-8e50-8dba03d3665c",
        "success": true
    },
    {
        "result": "234b05c3-00e6-46b1-9aa7-9da88ce962fd",
        "success": true
    }
]
```

If you navigate to the Credential Registry (http://localhost:8080) you can search for and view the loaded credentials (Ima Permit - the entity name).
