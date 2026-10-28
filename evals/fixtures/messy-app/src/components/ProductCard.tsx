export function ProductCard({ name, price }: { name: string; price: string }) {
  return (
    <div className="card" style={{ borderRadius: 6 }}>
      <img src="/img.png" alt="" style={{ width: "100%", borderRadius: 4 }} />
      <h3 style={{ fontSize: 18, fontWeight: 600, color: "#202124" }}>{name}</h3>
      <p style={{ color: "#5f6368", fontSize: 14 }}>{price}</p>
      <button className="btn" style={{ fontSize: 13 }}>Add to cart</button>
      <a className="btn btn-secondary" href="#">Details</a>
    </div>
  );
}
