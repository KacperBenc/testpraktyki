function setRequired(sectionId, enable) {
    document.querySelectorAll(`#${sectionId} input, #${sectionId} select`)
        .forEach(el => {
            el.required = enable;
        });
}

function hideAll() {
    [
        "adres_fields",
        "student_fields",
        "pracodawca_fields",
        "opiekun_fields",
        "pracownikbk_fields"
    ].forEach(id => {
        document.getElementById(id).className = "hidden";
        setRequired(id, false);
    });
}

function updateRoleFields() {
    hideAll();

    const role = document.getElementById("id_main-rola").value;

    if (role === "Student") {
        document.getElementById("student_fields").className = "visible";
        document.getElementById("adres_fields").className = "visible";

        setRequired("student_fields", true);
        setRequired("adres_fields", true);
    }

    if (role === "Pracodawca") {
        document.getElementById("pracodawca_fields").className = "visible";
        document.getElementById("adres_fields").className = "visible";

        setRequired("pracodawca_fields", true);
        setRequired("adres_fields", true);
    }

    if (role === "Opiekun Praktyk") {
        document.getElementById("opiekun_fields").className = "visible";
        document.getElementById("adres_fields").className = "visible";
        setRequired("opiekun_fields", true);
    }

    if (role === "Pracownik BK") {
        document.getElementById("pracownikbk_fields").className = "visible";
        document.getElementById("adres_fields").className = "visible";
        setRequired("pracownikbk_fields", true);
    }
}

// odśwież po załadowaniu
document.addEventListener("DOMContentLoaded", updateRoleFields);

// przełącz po zmianie roli
document.getElementById("id_main-rola").addEventListener("change", updateRoleFields);