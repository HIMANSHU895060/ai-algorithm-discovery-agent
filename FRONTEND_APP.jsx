import React, { useState } from 'react';
import { FiSearch, FiLoader, FiCheckCircle } from 'react-icons/fi';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    problem_type: 'sorting',
    input_size: 1000,
    constraints: { time_limit: 1.0 }
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'input_size' ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/discover', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!response.ok) throw new Error('Failed to discover');
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>🤖 AI Algorithm Discovery Agent</h1>
        <p style={styles.subtitle}>Discover & Optimize Algorithms with ML</p>
      </header>

      <main style={styles.main}>
        <div style={styles.grid}>
          <div style={styles.formContainer}>
            <h2 style={styles.formTitle}>⚙️ Discover Algorithm</h2>
            <form onSubmit={handleSubmit} style={styles.form}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Problem Type</label>
                <select name="problem_type" value={formData.problem_type} onChange={handleChange} style={styles.input}>
                  <option value="sorting">🔄 Sorting</option>
                  <option value="searching">🔍 Searching</option>
                  <option value="optimization">⚡ Optimization</option>
                  <option value="graph">🕸️ Graph</option>
                  <option value="dp">📊 Dynamic Programming</option>
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Input Size</label>
                <input type="number" name="input_size" value={formData.input_size} onChange={handleChange} style={styles.input} />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>⏱️ Time Limit (sec)</label>
                <input type="number" step="0.1" value={formData.constraints.time_limit} onChange={(e) => setFormData(prev => ({ ...prev, constraints: { ...prev.constraints, time_limit: parseFloat(e.target.value) || 1 } }))} style={styles.input} />
              </div>

              <button type="submit" disabled={loading} style={{...styles.button, opacity: loading ? 0.5 : 1}}>
                {loading ? 'Discovering...' : 'Discover Algorithm'}
              </button>
            </form>
          </div>

          <div style={styles.resultsContainer}>
            {error && <div style={styles.error}>Error: {error}</div>}

            {loading && (
              <div style={styles.loading}>
                <FiLoader style={styles.spinner} />
                <p>Discovering optimal algorithm...</p>
              </div>
            )}

            {results && !loading && (
              <div style={styles.resultCard}>
                <div style={styles.resultHeader}>
                  <FiCheckCircle style={styles.checkIcon} />
                  <h2 style={styles.algorithmName}>{results.algorithm}</h2>
                </div>

                <div style={styles.metrics}>
                  <div style={styles.metric}>
                    <p style={styles.metricLabel}>TIME COMPLEXITY</p>
                    <p style={styles.metricValue}>{results.time_complexity || 'O(n log n)'}</p>
                  </div>
                  <div style={styles.metric}>
                    <p style={styles.metricLabel}>SPACE COMPLEXITY</p>
                    <p style={styles.metricValue}>{results.space_complexity || 'O(1)'}</p>
                  </div>
                </div>

                <div style={styles.fitnessContainer}>
                  <p style={styles.metricLabel}>✨ FITNESS SCORE</p>
                  <div style={styles.progressBar}>
                    <div style={{...styles.progressFill, width: `${(results.fitness_score || 0.85) * 100}%`}} />
                  </div>
                  <p style={styles.fitnessValue}>{Math.round((results.fitness_score || 0.85) * 100)}%</p>
                </div>

                <div style={styles.timeContainer}>
                  <p style={styles.metricLabel}>⏰ ESTIMATED TIME</p>
                  <p style={styles.timeValue}>{(results.estimated_time || 0.045).toFixed(4)}s</p>
                </div>
              </div>
            )}

            {!results && !loading && !error && (
              <div style={styles.placeholder}>
                <p>👉 Select a problem type and click "Discover"</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', background: 'linear-gradient(to bottom right, #1e3a8a, #1e40af, #6b21a8)', fontFamily: 'Arial, sans-serif' },
  header: { background: 'rgba(0,0,0,0.3)', backdropFilter: 'blur(10px)', borderBottom: '1px solid #3b82f6', padding: '2rem', textAlign: 'center', color: 'white', position: 'sticky', top: 0, zIndex: 50 },
  title: { fontSize: '2rem', fontWeight: 'bold', margin: 0 },
  subtitle: { color: '#93c5fd', marginTop: '0.5rem', margin: '0.5rem 0 0 0' },
  main: { maxWidth: '80rem', margin: '0 auto', padding: '2rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' },
  formContainer: { background: 'rgba(30, 58, 138, 0.7)', border: '1px solid #3b82f6', borderRadius: '0.5rem', padding: '1.5rem', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)' },
  formTitle: { fontSize: '1.5rem', fontWeight: 'bold', color: 'white', marginTop: 0, marginBottom: '1rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  formGroup: { display: 'flex', flexDirection: 'column' },
  label: { color: '#93c5fd', fontWeight: '600', marginBottom: '0.5rem', fontSize: '0.9rem' },
  input: { padding: '0.5rem', background: '#1e3a8a', color: 'white', border: '1px solid #3b82f6', borderRadius: '0.375rem', fontSize: '1rem' },
  button: { background: 'linear-gradient(to right, #3b82f6, #7c3aed)', color: 'white', fontWeight: 'bold', padding: '0.75rem 1rem', borderRadius: '0.5rem', border: 'none', cursor: 'pointer', fontSize: '1rem' },
  resultsContainer: { minHeight: '400px' },
  error: { background: '#7c2d12', color: '#fed7aa', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #dc2626', marginBottom: '1rem' },
  loading: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '400px', background: '#1e3a8a', borderRadius: '0.5rem', border: '1px solid #3b82f6', color: '#93c5fd' },
  spinner: { fontSize: '3rem', animation: 'spin 1s linear infinite', marginBottom: '1rem' },
  resultCard: { background: 'linear-gradient(to bottom right, #15803d, #059669)', border: '1px solid #10b981', borderRadius: '0.5rem', padding: '1.5rem', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)' },
  resultHeader: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
  checkIcon: { fontSize: '2rem', color: '#4ade80' },
  algorithmName: { fontSize: '1.875rem', fontWeight: 'bold', color: 'white', margin: 0 },
  metrics: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' },
  metric: { background: 'rgba(0,0,0,0.3)', borderRadius: '0.375rem', padding: '1rem' },
  metricLabel: { color: '#86efac', fontSize: '0.875rem', fontWeight: '600', margin: 0 },
  metricValue: { color: 'white', fontSize: '1.5rem', fontFamily: 'monospace', fontWeight: 'bold', margin: '0.5rem 0 0 0' },
  fitnessContainer: { background: 'rgba(0,0,0,0.3)', borderRadius: '0.375rem', padding: '1rem', marginBottom: '1rem' },
  progressBar: { width: '100%', background: '#374151', borderRadius: '9999px', height: '1rem', overflow: 'hidden', marginTop: '0.5rem' },
  progressFill: { background: 'linear-gradient(to right, #facc15, #10b981, #059669)', height: '100%', transition: 'width 0.3s' },
  fitnessValue: { color: 'white', fontSize: '1.25rem', fontWeight: 'bold', marginTop: '0.5rem', margin: '0.5rem 0 0 0' },
  timeContainer: { background: 'rgba(0,0,0,0.3)', borderRadius: '0.375rem', padding: '1rem' },
  timeValue: { color: 'white', fontSize: '1.125rem', fontFamily: 'monospace', margin: '0.5rem 0 0 0' },
  placeholder: { display: 'flex', alignItems: 'center', justifyContent: 'center', height: '400px', background: 'rgba(30, 58, 138, 0.3)', borderRadius: '0.5rem', border: '2px dashed #3b82f6', color: '#93c5fd', fontSize: '1.125rem' }
};

export default App;
