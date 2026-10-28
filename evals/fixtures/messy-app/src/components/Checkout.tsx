export function Checkout() {
  return (
    <section className="checkout">
      <h1>Checkout</h1>
      <input type="text" placeholder="Name" />
      <input type="email" placeholder="Email" />
      <select><option>Card</option><option>Invoice</option></select>
      <p className="error">Something went wrong</p>
      <button className="primary-button">Pay now</button>
      <button className="cancel">Cancel</button>
    </section>
  );
}
