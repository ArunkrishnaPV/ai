// Function to handle Study Assistant submission
async function submitStudyQuestion(event) {
    event.preventDefault();
    
    const subject = document.getElementById('subject').value;
    const topic = document.getElementById('topic').value;
    const question = document.getElementById('question').value;
    
    const loading = document.getElementById('loading');
    const resultBox = document.getElementById('resultBox');
    const answerContent = document.getElementById('answerContent');
    
    // Show loading
    loading.style.display = 'block';
    resultBox.style.display = 'none';
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ subject, topic, question })
        });
        
        const data = await response.json();
        
        // Hide loading and show result
        loading.style.display = 'none';
        resultBox.style.display = 'block';
        
        // Format the text simple formatting for newlines
        answerContent.innerHTML = data.answer.replace(/\n/g, '<br>');
        
    } catch (error) {
        loading.style.display = 'none';
        resultBox.style.display = 'block';
        answerContent.innerHTML = "<span style='color:red;'>An error occurred while fetching the response. Please try again.</span>";
    }
}

// Function to handle Planner submission
async function submitPlanner(event) {
    event.preventDefault();
    
    const subject = document.getElementById('subject').value;
    const topics = document.getElementById('topics').value;
    const examDate = document.getElementById('examDate').value;
    const hours = document.getElementById('hours').value;
    const difficulty = document.getElementById('difficulty').value;
    
    const loading = document.getElementById('loading');
    const resultBox = document.getElementById('resultBox');
    const planContent = document.getElementById('planContent');
    
    loading.style.display = 'block';
    resultBox.style.display = 'none';
    
    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ subject, topics, examDate, hours, difficulty })
        });
        
        const data = await response.json();
        
        loading.style.display = 'none';
        resultBox.style.display = 'block';
        planContent.innerHTML = data.plan.replace(/\n/g, '<br>');
        
    } catch (error) {
        loading.style.display = 'none';
        resultBox.style.display = 'block';
        planContent.innerHTML = "<span style='color:red;'>An error occurred.</span>";
    }
}

// Function to load progress
async function loadProgress() {
    try {
        const response = await fetch('/api/progress');
        const data = await response.json();
        
        const progress = data.progress;
        document.getElementById('overallPercentage').textContent = progress.overall_percentage + '%';
        document.getElementById('progressBar').style.width = progress.overall_percentage + '%';
        
        const skillsList = document.getElementById('skillsList');
        skillsList.innerHTML = '';
        progress.skills.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = `${skill.name} (${skill.level})`;
            skillsList.appendChild(li);
        });
        
    } catch (error) {
        console.error("Error loading progress:", error);
    }
}

// Function to update progress
async function submitProgress(event) {
    event.preventDefault();
    
    const studentName = document.getElementById('studentName').value;
    const subject = document.getElementById('subject').value;
    const marks = document.getElementById('marks').value;
    const skill = document.getElementById('skill').value;
    const skillLevel = document.getElementById('skillLevel').value;
    
    try {
        const response = await fetch('/api/progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ studentName, subject, marks, skill, skillLevel })
        });
        
        const data = await response.json();
        alert(data.message);
        
        // Reload progress display
        loadProgress();
        document.getElementById('progressForm').reset();
        
    } catch (error) {
        alert("Failed to update progress.");
    }
}

// Auto load progress if on progress page
if (window.location.pathname === '/progress') {
    document.addEventListener('DOMContentLoaded', loadProgress);
}
