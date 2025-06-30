function generatePDF() {
    // Copy text to PDF content
    document.getElementById("pdf_name").textContent = document.getElementById("name").value;
    document.getElementById("pdf_father_name").textContent = document.getElementById("father_name").value;
    document.getElementById("pdf_district").textContent = document.getElementById("district").value;
    document.getElementById("pdf_block").textContent = document.getElementById("block").value;
    document.getElementById("pdf_village").textContent = document.getElementById("village").value;

    // Add member rows
    let tbody = document.getElementById("pdf_members");
    tbody.innerHTML = "";
    for (let i = 0; i < 5; i++) {
        let name = document.getElementById("member_name" + i).value;
        if (name) {
            let age = document.getElementById("member_age" + i).value;
            let gender = document.getElementById("member_gender" + i).value;
            let relation = document.getElementById("member_relation" + i).value;
            let row = `<tr>
                        <td>${i+1}</td>
                        <td>${name}</td>
                        <td>${age}</td>
                        <td>${gender}</td>
                        <td>${relation}</td>
                       </tr>`;
            tbody.innerHTML += row;
        }
    }

    // Show content and generate PDF
    document.getElementById("pdf-content").style.display = "block";
    html2pdf().from(document.getElementById("pdf-content")).save("ration_card.pdf");
}