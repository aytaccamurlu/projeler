"use client";
import { useState, useEffect } from "react";

export default function CRM() {
  const [customers, setCustomers] = useState([]);
  const [formData, setFormData] = useState({ name: "", email: "", phone: "", status: "Potansiyel" });
  const API_URL = "/api/customers";

  // Verileri Getir
  const fetchCustomers = async () => {
    const res = await fetch(API_URL);
    const data = await res.json();
    setCustomers(data);
  };

  useEffect(() => { fetchCustomers(); }, []);

  // Müşteri Ekle
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    setFormData({ name: "", email: "", phone: "", status: "Potansiyel" });
    fetchCustomers();
  };

  // Müşteri Sil
  const deleteCustomer = async (id: string) => {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchCustomers();
  };

  return (
    <main style={{ padding: "40px", fontFamily: "sans-serif", backgroundColor: "#f4f7f6", minHeight: "100vh" }}>
      <h1 style={{ color: "#2c3e50" }}>Müşteri Yönetim Sistemi (CRM)</h1>

      {/* Müşteri Ekleme Formu */}
      <section style={{ backgroundColor: "#fff", padding: "20px", borderRadius: "8px", marginBottom: "30px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)" }}>
        <h3>Yeni Müşteri Ekle</h3>
        <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
          <input placeholder="Ad Soyad" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required style={inputStyle} />
          <input placeholder="Email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required style={inputStyle} />
          <input placeholder="Telefon" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} style={inputStyle} />
          <select value={formData.status} onChange={e => setFormData({...formData, status: e.target.value})} style={inputStyle}>
            <option value="Potansiyel">Potansiyel</option>
            <option value="Ulaşıldı">Ulaşıldı</option>
            <option value="Satış Tamam">Satış Tamam</option>
          </select>
          <button type="submit" style={btnStyle}>Kaydet</button>
        </form>
      </section>

      {/* Müşteri Listesi */}
      <table style={{ width: "100%", borderCollapse: "collapse", backgroundColor: "#fff", borderRadius: "8px", overflow: "hidden" }}>
        <thead>
          <tr style={{ backgroundColor: "#2c3e50", color: "#fff", textAlign: "left" }}>
            <th style={thStyle}>Ad Soyad</th>
            <th style={thStyle}>Email</th>
            <th style={thStyle}>Telefon</th>
            <th style={thStyle}>Durum</th>
            <th style={thStyle}>İşlem</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c: any) => (
            <tr key={c._id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={tdStyle}>{c.name}</td>
              <td style={tdStyle}>{c.email}</td>
              <td style={tdStyle}>{c.phone}</td>
              <td style={tdStyle}>
                <span style={{ ...statusBadge, backgroundColor: c.status === "Satış Tamam" ? "#2ecc71" : "#f1c40f" }}>{c.status}</span>
              </td>
              <td style={tdStyle}>
                <button onClick={() => deleteCustomer(c._id)} style={{ color: "red", border: "none", cursor: "pointer", background: "none" }}>Sil</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

// Basit CSS stilleri
const inputStyle = { padding: "10px", borderRadius: "4px", border: "1px solid #ddd", flex: 1, minWidth: "150px" };
const btnStyle = { padding: "10px 20px", backgroundColor: "#3498db", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" };
const thStyle = { padding: "15px" };
const tdStyle = { padding: "15px" };
const statusBadge = { padding: "4px 8px", borderRadius: "12px", color: "white", fontSize: "12px" };