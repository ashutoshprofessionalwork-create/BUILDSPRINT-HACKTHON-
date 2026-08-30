## to run the webpage 

pip install django 
pip install pillow 

then in terminal open the blood_bank folder and use integrated terminal in it 
then run the command
python manage.py runserver <-- this is to show the ip and to run the server
 

pip install cohere 


to use danjgo admin panel just write /admin after the address

Name:- Sattwik
Password:-1234

##working flow

[1. Patient Submits Emergency Request]
   │
   ▼ (Captures blood group, locality, hospital, and condition notes)
[2. SkillPatch / AI Triage Evaluation]
   │
   ▼ (Analyzes medical text: trauma, ICU, and blood rarity to calculate urgency score)
[3. Real-Time Priority Queue]
 ----------------------------------------------------------------------------------------
 [1. Patient Submits Emergency Request]
   │
   ▼ (Captures blood group, locality, hospital, and clinical notes)
[2. AI Urgency & Semantic Triage]
   │
   ▼ (Evaluates medical severity, trauma, ICU need, and blood rarity)
[3. Real-Time Priority Queue]

----------------------------------------------------------------------------------------------
[1. Patient Registration & Sign In]
   │
   ▼ (Patient creates account credentials and signs into the platform)
[2. Post Blood Request]
   │
   ▼ (Patient submits specific blood group, hospital, and emergency details)
[3. Request Routed to Admin Panel]
   │
   ▼ (Request is hidden from public and donors to prevent spam/false alarms)
[4. Admin Reviews & Approves]
   │
   ▼ (Admin audits the medical need and approves the case with a single click)
[5. Broadcast to Donors & Live Home Feed]
   │
   ▼ (Verified request becomes visible on the homepage and notifies matching donors)
[6. Donor Connection & Fulfillment]
