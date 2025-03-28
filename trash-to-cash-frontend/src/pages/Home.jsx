import React, { useState } from 'react';

import {
  uploadImage,
  updateClassification,
  updateRecyclingCount,
} from "../services/api";
import './Home.css';
function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return setError("Please select an image!");
    setError("");
    setLoading(true);

    const data = {
      image_path: selectedFile.name,
      user_id: "user123",
    };

    try {
      const response = await uploadImage(data);
      setResult(response.data);
    } catch {
      setError("Failed to upload image.");
    } finally {
      setLoading(false);
    }
  };

  const handleAIClassification = async () => {
    setLoading(true);
    const classificationData = {
      image_path: selectedFile.name,
      material_type: "Plastic",
      recyclable: true,
      price: 0.25,
      triangle_code: "1",
    };
    try {
      await updateClassification(classificationData);
      setResult({ ...result, ...classificationData });
    } catch {
      setError("Classification failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStats = async () => {
    try {
      await updateRecyclingCount("user123", "Plastic");
      alert("✅ Recycling count updated!");
    } catch {
      setError("Update failed.");
    }
  };

  const handleCameraScan = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = document.createElement("video");
      video.srcObject = stream;
      video.setAttribute("autoplay", true);
      video.setAttribute("playsinline", true);
      video.style.maxWidth = "90%";
      video.style.borderRadius = "10px";
      video.style.boxShadow = "0 4px 20px rgba(0,0,0,0.5)";
  
      const overlay = document.createElement("div");
      overlay.style.position = "fixed";
      overlay.style.top = 0;
      overlay.style.left = 0;
      overlay.style.width = "100vw";
      overlay.style.height = "100vh";
      overlay.style.background = "rgba(0, 0, 0, 0.85)";
      overlay.style.display = "flex";
      overlay.style.flexDirection = "column";
      overlay.style.justifyContent = "center";
      overlay.style.alignItems = "center";
      overlay.style.zIndex = "9999";
  
      const controls = document.createElement("div");
      controls.style.display = "flex";
      controls.style.justifyContent = "center";
      controls.style.gap = "20px";
      controls.style.marginTop = "20px";
  
      const captureBtn = document.createElement("button");
      captureBtn.innerText = "📸 Capture";
      captureBtn.style.padding = "12px 24px";
      captureBtn.style.fontSize = "18px";
      captureBtn.style.borderRadius = "8px";
      captureBtn.style.border = "none";
      captureBtn.style.cursor = "pointer";
      captureBtn.style.background = "#38a169";
      captureBtn.style.color = "#fff";
      captureBtn.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
  
      const cancelBtn = document.createElement("button");
      cancelBtn.innerText = "❌ Cancel";
      cancelBtn.style.padding = "12px 24px";
      cancelBtn.style.fontSize = "18px";
      cancelBtn.style.borderRadius = "8px";
      cancelBtn.style.border = "none";
      cancelBtn.style.cursor = "pointer";
      cancelBtn.style.background = "#e53e3e";
      cancelBtn.style.color = "#fff";
      cancelBtn.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
  
      overlay.appendChild(video);
      controls.appendChild(captureBtn);
      controls.appendChild(cancelBtn);
      overlay.appendChild(controls);
      document.body.appendChild(overlay);
  
      // Capture logic
      captureBtn.onclick = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        canvas.toBlob((blob) => {
          const file = new File([blob], "scanned-bottle.png", { type: "image/png" });
          setSelectedFile(file);
        });
        cleanup();
      };
  
      // Cancel logic
      cancelBtn.onclick = () => {
        cleanup();
      };
  
      // Stop camera & remove overlay
      const cleanup = () => {
        video.pause();
        stream.getTracks().forEach((track) => track.stop());
        document.body.removeChild(overlay);
      };
    } catch (err) {
      setError("Camera access denied or not supported.");
    }
  };
  





  return (
  <div className="home-wrapper">
    <div className="home-navbar">
      <h1>♻️ Trash to Cash</h1>
      <div>
        <button className="nav-btn">Login</button>
        <button className="nav-btn">Sign Up</button>
      </div>
    </div>

    <div className="eco-phrase">
      🌍 "Turning Waste into Wealth. Stay Eco-Friendly!" 🌱
    </div>

    <div className="home-content">
      <input type="file" onChange={handleFileChange} />
      {selectedFile && (
        <div>
          <img
            src={URL.createObjectURL(selectedFile)}
            alt="Preview"
            className="preview-image"
          />
        </div>
      )}

      <button onClick={handleUpload}>📤 Upload Bottle Image</button>
      <button onClick={handleCameraScan}>📷 Scan Bottle via Camera</button>

      <button onClick={handleAIClassification}>🧠 Run AI Classification</button>
      <button onClick={handleUpdateStats}>📈 Update Recycling Stats</button>

      {loading && <p>⏳ Processing...</p>}
      {error && <p className="error-message">{error}</p>}

      {result && (
        <div className="result-box">
          <h3>✅ Classification Result</h3>
          <p><strong>Material:</strong> {result.material_type}</p>
          <p><strong>Recyclable:</strong> {result.recyclable ? "Yes" : "No"}</p>
          <p><strong>Price:</strong> ${result.price}</p>
        </div>
      )}
    </div>
  </div>
);

}



export default Home;
