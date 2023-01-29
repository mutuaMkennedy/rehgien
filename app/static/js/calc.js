//mortgage calc code
//the formular: c= ((p*r) * Math.pow((1+r), n)) / (Math.pow((1+r), n) - 1)
//@param p float Amount borrowed
//@param r interest r interest as a percentage
//@param n term in years
function calculateMortgage(p, r, n) {

	//var monthlyPayments = null;

	//convert this percentage to a decimal
	r = percentToDecimal(r);

	//convert years to months
	n = yearsToMonths(n);

	var pmt = (r*p) / (1 - (Math.pow((1+r), (-n))));

	return parseFloat(pmt.toFixed(2));
}	

function percentToDecimal(percent) {
	return (percent/12)/100;
}

function yearsToMonths(years) {
	return years * 12;
}

function postPayments(payment) {
	var htmlEl = document.getElementById("outMonthly");

	htmlEl.innerText = "Kshs." + payment;
}

var btn = document.getElementById("btnCalculate");
btn.onclick = function() {
	var amount = document.getElementById("inAmount").value;
	var downPayment = document.getElementById("inDown").value;
	var interest = document.getElementById("inAPR").value;
	var period = document.getElementById("inPeriod").value;

	console.log(amount, downPayment, interest, period);

	var amountBorrowed = amount - downPayment;
	console.log(amountBorrowed, interest, period);

	var pmt = calculateMortgage(amountBorrowed, interest, period);
	postPayments(pmt);
};