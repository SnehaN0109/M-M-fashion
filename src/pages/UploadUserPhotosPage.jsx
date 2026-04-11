const UploadUserPhotosPage = () => {
  return (
    <div className="max-w-md mx-auto px-6 py-16">
      <h1 className="text-2xl font-bold mb-6">
        Upload Your Garba Look 📸
      </h1>

      <input
        type="file"
        className="border p-3 w-full mb-4"
      />

      <textarea
        placeholder="Write a short review (optional)"
        className="border p-3 w-full mb-4"
      />

      <button className="w-full bg-pink-600 text-white py-3 rounded">
        Submit Photo
      </button>
    </div>
  );
};

export default UploadUserPhotosPage;
