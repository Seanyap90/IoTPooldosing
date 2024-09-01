<h1>Pool Management Software</h1>

<h2>Background</h2>
<p>Despite a good start where the company I found secured early contracts from 3 customers for using DosAuto, we are unable to get meaningful traction.  Hence it was back to the drawing board on how to get the business going again. 
 Unfortunately, there was a huge disagreement among the cofounders on the strategic direction, so we decided to stick on what may seem to work according to gut instinct and whatever joint amount of experience we have.</p>
<p>Nontheless my vision to expand DosAuto was to develop a unified enterpise software for pool management that could bring a host of new business activities and organisational change to customers like single man pool cleaners, pool management companies themselves, pool equipment distributors and facility management companies</p>

<p>This repo will mainly showcase how I use cloud and other relevant technologies to build this software to deliever the below mentioned activities</p>

<h2>Enterprise Architecture v1.0</h2>

![PoolMgtEnterpriseArchitecture](https://github.com/user-attachments/assets/39a7e70e-c15d-4e3f-aa36-217327327fdd)

<p>To enable an earnest digital transformation for pool management as an industry in general, the following suggested approaches can be considered:
</p>

- Lowering risk of adopting new business activities
- Streamlining operations and upgrade staff's skills and capabilities with digital technologies
- Resource Planning
- Exploration of shared responsibility concept between pool maintnenace/management and their clients to understand implications and need payoffs for value increment and minimisation of costs

Value stream mapping could be useful in quantifying point 2, and 4 with data from IoT devices and senors, with visualisation and analytics

<h2>Requirements and Assumptions</h2>

<h3>Background Information</h3>

<p>In the pool management industry, service providers range from one man pool cleaners or small pool maintenance crews, 1 stop pool management companies and facility management companies.  Suggested approach is to split between basic and enterprise user plans</p>
<p>For the time being, the plans will be differentiated on the number of pools, access to customer support and reporting services.  Role based access will be available for enterprise version as targeted segment of pool management and facility management companies will have different kinds of users so we will assign roles such as operator, administrator & viewer.</p>
<p>When we add services (in form of business logic, functions or microservices) to support more business activities via this application, the differentiation could be more granular</p>

<h3>Business Requirements and Assumptions</h3>

- Basic plan and enterprise plan to be primarily differentatied via number of pools
- For DosAuto, assume 1 set of 2 dosing pumps and sensors will be used for 1 pool

<h3>User based Requirements and Assumptions</h3>

- Assume single man pool cleaners and other small pool maintenance crews will use basic plan, so they are unlikely to have enough staff for different functionalities
- For enterprise plan, there will be clear distinction between operator, administrator and viewer.
- Pool management companies may want to share specific data (real time or in analytics) with their clients for exploration of shared responsibility concept

<h2>High Level System Architecture v1.0: Building from DosAuto</h2>

![PoolmgtArchi_V1](https://github.com/user-attachments/assets/bdf0a4b2-5e5a-452e-88d0-5e294e5b67c9)

<h3>At the swimming pool</h3>
<p>DosAuto originally consisted of monitoring and automation modules.  Both modules consisted of a raspberry pi and other electronic components, where servers were residing for the application.  However moving forward, we will streamline the system setup to an edge gateway and end devices with either sensors or automation.  The edge gateway can add as both a MQTT broker for end devices to publish or receive data while a forwarder for data transfer onto cloud platforms such as AWS IoT Core.  We can also consider having end devices be equipped with LCD displays to assist any onsite operations.</p>

<h3>Cloud side</h3>

<h4>Summary: Adoption of Modular Monolith</h4>
<p>For version 1.0, we adopt the modular monolith architecture to organise functionalities such as real time operations (monitoring and dosing), reporting and remote support into modules so that each of them do not affect the application if one goes into error.  The database will be shared to ensure consistency and easier transaction management.  To add on other services such as predictive maintenance and various computer vision based services for pool security and safety, microservices can be considered</p>

<h4>Message Broker, Datastream and Database</h4>

<h4>Data storage</h4>
<p>A common data storage to store all IoT and sensor data for this application</p>

<h4>Business Logics</h4>
<p>For facilitating real time operations as well as any other real time elements on the client, we will preliminarily make use of serverless and in memory storage (such as Redis).  For analytics and reporting, serverless as well as IoT analytics can be utilised for pipelines</p>


<h3>Client</h3>

<h4>Registration and Login</h4>
<p>We can explore using Cognito, AWS Signature V4 or a custom authentication process to meet the requirements of providing basic and enterpise plans as well as role based user access for the latter</p>


