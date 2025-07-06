const jwt = require("jsonwebtoken");

const SECRET_KEY = "your-super-secret-key-here";

const payload = {
    userId: 123,
    email: "user@example.com"
};

const options = {
    expiresIn: "1h",
    issuer: "my-app",
    audience: "my-users", 
    subject: "authentication",
    algorithm: "none" // ใช้ 'none' เพื่อไม่ต้องการตรวจสอบ signature
};

// สร้าง token
const token = jwt.sign(payload, SECRET_KEY, options);
console.log("Token:", token);

// ถอดรหัส token (ไม่ตรวจสอบ signature)
const decoded = jwt.decode(token, { complete: true });
console.log("Decoded token:", decoded);
console.log("Decoded header:", decoded.header);
console.log("Decoded payload:", decoded.payload);

// ตรวจสอบ token (ตรวจสอบ signature)
try {
    // const user = jwt.verify(token, SECRET_KEY, {
    //     algorithms: [options.algorithm],
    //     issuer: options.issuer,
    //     audience: options.audience,
    //     subject: options.subject
    // });
    // console.log("Verified user:", user);
    const user2 = jwt.verify(token, null, {
        algorithms: [options.algorithm],
        issuer: options.issuer,
        audience: options.audience,
        subject: options.subject
    });
    console.log("Verified user2:", user2);
} catch (error) {
    console.log("Verification error:", error.message);
}