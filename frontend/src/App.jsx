import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [formData, setFormData] = useState({
    name: '',
    father_name: '',
    mobile_no: ''
  })
  const [errors, setErrors] = useState({})
  const [successMessage, setSuccessMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
    if (successMessage) setSuccessMessage('')
  }

  const validate = () => {
    const newErrors = {}
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    }
    
    if (!formData.father_name.trim()) {
      newErrors.father_name = 'Father name is required'
    }
    
    if (!formData.mobile_no.trim()) {
      newErrors.mobile_no = 'Mobile number is required'
    } else if (!/^\d{10}$/.test(formData.mobile_no)) {
      newErrors.mobile_no = 'Mobile number must be exactly 10 digits'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validate()) return

    setLoading(true)
    setSuccessMessage('')

    try {
      await axios.post(`${API_URL}/users`, formData)
      setSuccessMessage('User data saved successfully!')
      setFormData({ name: '', father_name: '', mobile_no: '' })
      setErrors({})
    } catch (err) {
      setErrors({ submit: err.response?.data?.detail || 'Failed to save. Please try again.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="form-card">
        <h1 className="form-title">User Registration</h1>
        <p className="form-subtitle">Enter your details below</p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your name"
              className={errors.name ? 'input-error' : ''}
            />
            {errors.name && <span className="error-text">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="father_name">Father Name</label>
            <input
              type="text"
              id="father_name"
              name="father_name"
              value={formData.father_name}
              onChange={handleChange}
              placeholder="Enter father's name"
              className={errors.father_name ? 'input-error' : ''}
            />
            {errors.father_name && <span className="error-text">{errors.father_name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="mobile_no">Mobile Number</label>
            <input
              type="text"
              id="mobile_no"
              name="mobile_no"
              value={formData.mobile_no}
              onChange={handleChange}
              placeholder="10 digit mobile number"
              maxLength={10}
              inputMode="numeric"
              className={errors.mobile_no ? 'input-error' : ''}
            />
            {errors.mobile_no && <span className="error-text">{errors.mobile_no}</span>}
          </div>

          {errors.submit && <div className="error-banner">{errors.submit}</div>}
          {successMessage && <div className="success-banner">{successMessage}</div>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Saving...' : 'Submit'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App






// dataentry/
// ├── frontend/           # React + Vite
// │   ├── src/
// │   │   ├── App.jsx     # Form with validation, Axios POST
// │   │   ├── App.css     # Card layout, responsive styles
// │   │   ├── main.jsx
// │   │   └── index.css
// │   ├── package.json
// │   ├── vite.config.js
// │   └── .env.example
// ├── backend/            # FastAPI
// │   ├── main.py        # POST /users, Supabase, CORS
// │   ├── requirments.txt
// │   └── .env.example
// ├── .env.example
// ├── .gitignore
// └── README.md


// SUPABASE_URL=https://tvosugusswmhitcphcmq.supabase.co
// SUPABASE_KEY=sb_publishable_bDbkKXrNiYK2Z1UxqeZWog_To6AjowZ