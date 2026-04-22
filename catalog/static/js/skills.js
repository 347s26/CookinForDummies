const e = React.createElement;

function SkillCard({ skill }) {
    return e(
        "div",
        { className: "recipe-card" },
        e("div", { className: skill.image ? "recipe-card-image" : "recipe-card-image recipe-card-image-placeholder",
            style: skill.image
                ? { backgroundImage: "url('" + skill.image + "')", backgroundSize: "cover", backgroundPosition: "center" }
                : {}
         }),
        e("div", { className: "recipe-card-bottom" },
            e("p", { className: "recipe-title" }, skill.name),
            skill.video && e("div", { className: "recipe-meta" },
                e("a", { href: skill.video, target: "_blank", rel: "noreferrer", style: { color: "#d4a870", textDecoration: "none" } }, "Watch video ›")
            )
        )
    );
}

function SkillsApp() {
    return e(
        "div",
        null,
        e("div", { className: "section-header" },
            e("h2", { className: "section-title" }, "All Skills")),
        e("div", { className: "recipe-list" },
            SKILLS.map(skill => e(SkillCard, { key: skill.id, skill }))
        )
    );
}

ReactDOM.createRoot(document.getElementById("react-skills")).render(e(SkillsApp));
