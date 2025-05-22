function bookFlight(from, to, price, seatClass, date, time) {
  const payload = {
    name: "Besty",
    from: from,
    to: to,
    price: price,
    seatClass: seatClass,
    date: date,
    time: time
  };
  console.log("📦 Booking Data:", payload);
  fetch("https://flyhigh-backend.onrender.com/book-flight", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
})

  .then(res => res.json())
  .then(data => {
    if (data.url) window.location.href = data.url;
  })
  .catch(err => {
    console.error("Stripe checkout error:", err);
    alert("⚠️ Something went wrong.");
  });
}