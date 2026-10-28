export function Header() {
  return (
    <header style={{ padding: 12, background: "#fafafa", borderBottom: "1px solid #e0e0e0" }}>
      <a href="/" className="logo">Shop</a>
      <nav><a href="/products">Products</a><a href="/account">Account</a></nav>
      <form role="search"><label htmlFor="q">Search</label><input id="q" type="search" /><button className="btn">Go</button></form>
    </header>
  );
}
