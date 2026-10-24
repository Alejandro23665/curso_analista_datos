export default function ProgressRing({ value = 0, size = 132, stroke = 11, label = "completado" }) {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - Math.min(Math.max(value, 0), 100) / 100);
  return (
    <div className="ring" style={{ width: size, height: size }}>
      <svg width={size} height={size} role="img" aria-label={value + "% " + label}>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="var(--line)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--green)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={"rotate(-90 " + size / 2 + " " + size / 2 + ")"}
          style={{ transition: "stroke-dashoffset .6s ease" }}
        />
      </svg>
      <div className="ring-text">
        <strong>{value}%</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}
