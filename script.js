const { spawn } = require('child_process');

function runPythonScript() {
  // Show the loading spinner
  document.getElementById("loading-spinner").style.display = "block";

  // Get the domain and email values from the form
  const domain = document.getElementById("domain").value;
  const email = document.getElementById("email").value;
  
  // Run the Python script
  const script = spawn('python', ['/path/to/script.py', domain, email]);
  
  script.stdout.on('data', (data) => {
    // Do something with the data returned from the script
    console.log(data);
  });
  script.stderr.on('data', (data) => {
    // Handle any errors that occur
    console.error(data);
  });

  script.on('close', (code) => {
    // Hide the loading spinner
    document.getElementById("loading-spinner").style.display = "none";
  });
}
