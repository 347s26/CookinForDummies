const e = React.createElement;

function SkillCard({ skill }) {
    return e(
        "div",
        { className: "recipe-card" },
        e("div", { className: "recipe-card-image" }),
        e("div", { className: "recipe-card-bottom" },
            e("p", { className: "recipe-title" }, skill.name),
            skill.video && e("p", { className: "recipe-meta" },
                e("a", { href: skill.video, target: "_blank", rel: "noreferrer", style: { color: "#467f5a", textDecoration: "none" } }, "Watch video ›")
            )
        )
    );
}

function SkillsApp() {
    return e(
        "div",
        null,
        e("h2", { className: "section-title" }, "Skills"),
        e("div", { className: "recipe-list" },
            SKILLS.map(skill => e(SkillCard, { key: skill.id, skill }))
        )
    );
}

ReactDOM.createRoot(document.getElementById("react-skills")).render(e(SkillsApp));
