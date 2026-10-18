dashboard_html_str = """
<html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>This is the predictions dashboard for nurses!</h1>
        <p>Patient data does not survive Docker restarts, as a persistent data store was assumed to be out of scope for this assignment.</p>
        <div>
        <h3>Are you a nurse and don't got an ID?</h3>
        <button id="generateNurseIdBtn">Generate a new ID</button>
        <p id="generatedNurseId"></p>
        </div>
        <div>
        <h3>Register a new prediction for your patient</h3>
        <form id="predictionForm">
        <input id="nurseIdInput" type="text" placeholder="Your nurse ID" required>
        <input id="patientIdInput" type="text" placeholder="Your patient's ID" required>
        <input id="ageInput" type="number" placeholder="Age" required>
        <input id="sexInput" type="number" placeholder="Sex" required>
        <input id="bmiInput" type="number" placeholder="BMI" required>
        <input id="bpInput" type="number" placeholder="Blood pressure" required>
        <input id="s1Input" type="number" placeholder="s1" required>
        <input id="s2Input" type="number" placeholder="s2" required>
        <input id="s3Input" type="number" placeholder="s3" required>
        <input id="s4Input" type="number" placeholder="s4" required>
        <input id="s5Input" type="number" placeholder="s5" required>
        <input id="s6Input" type="number" placeholder="s6" required>
        <button type="submit">Generate prediction</button>
        
        <p id="generatedPatientPrediction"></p>
        </form>
        <div>
        </div>
        <h3>Your Patient Records (descending)</h3>
        <form id="loadPatientsForm">
        <input id="nurseIdTableInput" type="text" placeholder="Your Nurse ID" required></input>
        <select id="sortingOrder">
        <option value="descending">Descending</option>
        <option value="ascending">Ascending</option>
        </select>
        <button type="submit">Load patients</button>
        </form>
        <table>
        <thead><tr><th>Patient ID</th><th>Prediction</th><th>Patient Input Values</th></tr></thead>
        <tbody id="patientsBody"></tbody>
        </table>
        </div>
    </body>
    
    <script>
    let nurseId = null;
    let prediction = null;
    let patientPredictions = [];
    
    const generatedNurseIdEl = document.getElementById("generatedNurseId");
    const generatedPredictionEl = document.getElementById("generatedPatientPrediction");
    
    async function fetchNursePatients() {
        const nurseId = document.getElementById("nurseIdTableInput").value;
        const sortingOrder = document.getElementById("sortingOrder").value;
        
        const response = await fetch(`/nurse/${nurseId}/patients?sorting_order=${sortingOrder}`);
        const patients = await response.json();
        
        const tableBody = document.getElementById("patientsBody");
        
        tableBody.innerHTML = "";
        
        patients.predictions.forEach((patient) => {
            const row = tableBody.insertRow();
            row.insertCell().textContent = patient.id;
            row.insertCell().textContent = patient.prediction;
            row.insertCell().textContent = JSON.stringify(patient.patient_input_values);
        });
    }
    
    async function generateNurseId() {
        const response = await fetch(`/generate-nurse-id`);
        nurseId = await response.json();
        
        generatedNurseIdEl.textContent = `  ${nurseId}  - This is your nurse ID. Paste this when making calls.`
    }
    
    async function generatePrediction() {
        const nurseId = document.getElementById("nurseIdInput").value;
        const patientId = document.getElementById("patientIdInput").value;
        const age = Number(document.getElementById("ageInput").value);
        const sex = Number(document.getElementById("sexInput").value);
        const bmi = Number(document.getElementById("bmiInput").value);
        const bp = Number(document.getElementById("bpInput").value);
        const s1 = Number(document.getElementById("s1Input").value);
        const s2 = Number(document.getElementById("s2Input").value);
        const s3 = Number(document.getElementById("s3Input").value);
        const s4 = Number(document.getElementById("s4Input").value);
        const s5 = Number(document.getElementById("s5Input").value);
        const s6 = Number(document.getElementById("s6Input").value);
        
        const response = await fetch(`/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nurse_id: nurseId,
                patient_id: patientId,
                age, sex, bmi, bp, s1, s2, s3, s4, s5, s6,
            }),
        });
        const predictionResponse = await response.json();
        prediction = predictionResponse["prediction"];
        
        generatedPredictionEl.textContent = `Prediction for patient ${patientId} is: ${prediction}. \n Reload your patients to see this patient.`;
        
    }
    
    const generateNurseIdBtn = document.getElementById("generateNurseIdBtn");
    
    generateNurseIdBtn.addEventListener("click", generateNurseId);
    document.getElementById("predictionForm").addEventListener("submit", (event) => {
        event.preventDefault();
        generatePrediction();
    });
    document.getElementById("loadPatientsForm").addEventListener("submit", (event) => {
        event.preventDefault();
        fetchNursePatients();
    });
    
    </script>
</html>
"""