const houses = [
  { id: 1, name: "Blue Haven Apartment", size: "75 sqm", price: 16000, occupied: false, image: "/static/images/house1.jpg" },
  { id: 2, name: "Sunset Villa", size: "80 sqm", price: 17000, occupied: true, image: "/static/images/house2.jpg" },
  { id: 3, name: "Hilltop Residence", size: "70 sqm", price: 15500, occupied: false, image: "/static/images/house3.jpg" },
  { id: 4, name: "Palm Court Home", size: "90 sqm", price: 18500, occupied: true, image: "/static/images/house4.jpg" },
  { id: 5, name: "Garden View House", size: "85 sqm", price: 17800, occupied: false, image: "/static/images/house5.jpg" },
];

function HouseCard({ house, onClick }) {
  return (
    <div className="house-card" onClick={() => onClick(house)}>
      <img src={house.image} alt={house.name} className="house-image" />
      <div className="house-info">
        <h3>{house.name}</h3>
        <p>Size: {house.size}</p>
        <p>Price: ₱{house.price.toLocaleString()}</p>
        <p className="status">{house.occupied ? "Occupied" : "Available"}</p>
      </div>
    </div>
  );
}

function HouseModal({ house, onClose }) {
  if (!house) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <img src={house.image} alt={house.name} className="modal-image" />
        <h2>{house.name}</h2>
        <p><strong>Size:</strong> {house.size}</p>
        <p><strong>Price:</strong> ₱{house.price.toLocaleString()}</p>
        <p><strong>Status:</strong> <span className="status">{house.occupied ? "Occupied" : "Available"}</span></p>
        <button className="close-btn" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

function Houses() {
  const [selectedHouse, setSelectedHouse] = React.useState(null);
  return (
    <>
      <div className="house-container">
        {houses.map(h => <HouseCard key={h.id} house={h} onClick={setSelectedHouse} />)}
      </div>
      <HouseModal house={selectedHouse} onClose={() => setSelectedHouse(null)} />
    </>
  );
}

ReactDOM.createRoot(document.getElementById("houses-root")).render(<Houses />);
