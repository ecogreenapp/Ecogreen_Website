-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 17, 2024 at 01:51 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecogreendb`
--

-- --------------------------------------------------------

--
-- Table structure for table `artikel`
--

CREATE TABLE `artikel` (
  `id` int(11) UNSIGNED NOT NULL,
  `judul` varchar(255) NOT NULL,
  `gambar` varchar(225) NOT NULL,
  `isi_artikel` text NOT NULL,
  `kategori` varchar(100) NOT NULL,
  `tanggal` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `artikel`
--

INSERT INTO `artikel` (`id`, `judul`, `gambar`, `isi_artikel`, `kategori`, `tanggal`) VALUES
(2, 'Apa itu Ecogreen?', 'uploads/artikel/artikel1.png', 'Ecogreen merupakan solusi pengelolaan sampah sebagai edukasi dan peluang bisnis bagi ibu rumah tangga. Ecogreen memiliki 3 fitur menarik menggunakan AI yaitu fitur deteksi sampah (trashtec), fitur chatbot (greenbot), dan fitur sentimen analisis.', 'Berita', '2024-01-15'),
(6, 'Sampah Adalah Bencana Bagi Lingkungan', 'uploads\\artikel\\artikel2.png', 'Dampak sampah bagi lingkungan adalah', 'Berita', '2024-01-15'),
(7, 'Langkah Tepat Penanganan Sampah', 'uploads\\artikel\\artikel3.png', 'Penanganan yang tidak tepat ke akar masalah dan menyebabkan dampak negatif sampah terus terjadi', 'Berita', '2024-01-16');

-- --------------------------------------------------------

--
-- Table structure for table `banksampah`
--

CREATE TABLE `banksampah` (
  `id` int(10) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `alamat` varchar(250) DEFAULT NULL,
  `pj` varchar(50) DEFAULT NULL,
  `no_hp` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `banksampah`
--

INSERT INTO `banksampah` (`id`, `nama`, `alamat`, `pj`, `no_hp`) VALUES
(6, 'Bank Sampah Mawar Biru', 'Jl. Rambutan Gg 11 RT 10 / RW 05, Kraton, Tegal\r\nBarat, Kota Tegal', 'Nurlaelatul Aqifah', '81902668645'),
(7, 'Bank Sampah Kalpataru', 'Jl. Nila No 11, Tegalsari, Tegal Barat, Kota Tegal - 52111', 'Indriani Winarti', '81249337302'),
(8, 'Bank Sampah Bianglala', 'Jl. Sawo Barat No 115, Kraton, Tegal Barat, Kota Tegal', 'Sabar Restani', '81542181393'),
(9, 'Bank Sampah Mekar Jaya', 'Balai RW IX Jl. Saparua No 13 RT 14 / RW 09,\r\nPanggung, Tegal Timur, Kota Tegal', 'Wariah', '81548119723'),
(10, 'Bank Sampah Berkah Amanah', 'Jl. Perintis Kemerdekaan Gg Raharjo I No 31 RT 03 /\r\nRW 12, Panggung, Tegak Timur, Kota Tegal', 'Susi Ariyani', '81542044267'),
(11, 'Bank Sampah Resik Barokah', 'Jl. Kudus RT 03 / RW 02, Debong Tengah, Tegal\r\nSelatan, Kota Tegal', 'Nur Khasanah', '818294386'),
(12, 'Bank Sampah Berseri', 'Jl. Prof Buyahamka RT 01 / RW 10, Margadana,\r\nMargadana, Kota Tegal', 'Sulistyaning Pudyastuti', '87720000942'),
(13, 'Bank Sampah Bahtera', 'Jl. Sipayung Raya RT 05 / RW 12, Panggung, Tegal\r\nTimur, Kota Tegal', 'Endang Winarsih', '85869168343'),
(14, 'Bank Sampah Puter', 'Jl. Puter No 19 RT 01 / RW 03, Randuguntng, Tegal\r\nSelatan, Kota Tegal', 'Sri Mulyani', '83839324551'),
(15, 'Bank Sampah Berkah Sakti', 'Jl. Palopo RT 06 / RW 01, Tunon, Tegal Selatan, Kota\r\nTegal', 'Tri Setyowati', '85869267677'),
(16, 'Bank Sampah Nusa Indah', 'Perum Tegal Residence Fasum Blok B1 RT 02 / RW\r\n04 , Debong Kulon, Tegal Selatan, Kota Tegal', 'Siwi Nurbiajanti', '81228090956'),
(17, 'Bank Sampah Sakti Sahara', 'Jl. Sangir No 1 Kompleks OW PAI, Mintaragen, Tegal', 'Dr. Yusqon, M.Pd', '8156551420'),
(18, 'Bank Sampah Kemunclig', 'Jl. Kemuning 131A RT 02 / RW 06, Slerok, Tegal Timur,', 'Santoso', '85742550001'),
(19, 'Bank Sampah Edelweis', 'Jl. Metro RT 02 / RW 01, Debong kulon, Tegal Selatan,', 'Yuni Setianingsih', '89504044406'),
(20, 'Bank Sampah Dahlia', 'Jl. Dewi Sartiks No 72 RT 01 / RW 01, Debong Kulon,', 'Ulfi Nurohmianingsih', '8,82007E+11'),
(21, 'Bank Sampah Puter 06', 'Jl. Puter Gg 6 RT 06 / RW 03, Randugunting, Tegal', 'Ani Ismoyo Wati', '85870131730'),
(22, 'Bank Sampah Amanah', 'Jl. Kendari RT 02 / RW 03, Tunon, Tegal Selatan, Kota', 'Musriyah', '81389423728'),
(23, 'Bank sampah Ketilang', 'Jln.Nuri - Randugunting - Tegal Selatan', 'Dewi Rosita', '85290281815'),
(24, 'Bank Sampah Mawar Merah', 'Jl.Mujaher No.6 RT 01/RW 05 Tegalsari Tegal Barat', 'Andriyani', '85742000743'),
(25, 'Bank Sampah Fatmawati', 'Jl.KH.Nahrawi No.12 RT.05 / RW 04 Mangkukusuman', 'Marinah Wahyuningsih', '85866240360'),
(26, 'Bank Sampah Cendrawasih Jaya Bersinar', 'Jln.AR.Hakim Gg 19 No.2 RT 01/RW 08 - Randugunting', 'Urif Sofiyatun', '85641218008'),
(27, 'Bank Sampah Arum Jaya Bersinar', 'Jl. Arum no.26 - Randugunting', 'Endang Sri Rachmawati', '85600591762'),
(28, 'Bank Sampah Bersih Sehat', 'Jl.Samandikun Gg.3B RT 02/RW 03 -Debong Kulon', 'Riyatin', '85600211696'),
(29, 'Bank Sampah Metro Permai', 'Jln.Metro- Kel.Debong Lor', 'Adi Christiono', '85742551110'),
(30, 'Bank Sampah Merpati', 'Jl.Merpati Gg.Larwo RT.09/RW 02 - Randugunting', 'Suryani', '85742804765'),
(31, 'Bank Sampah Adem Sejahtera', 'Jl.Sipelem no.2 - Kraton- Tegal Barat', 'Endah Pratiwi', '81912224910'),
(32, 'Bank Sampah Prepil Berkah', 'Jl.Werkudoro RW.05 - Slerok -Tegal Timur', 'Fatmawati', '85642609367'),
(33, 'Bank Sampah RW. 01', 'Jl.Tentara Pelajar RW.01 -Slerok - Tegal Timur', 'Rini Sugiarto', '85642906019'),
(34, 'Bank Sampah Kemuning', 'RT.04 / RW.03 - Keturen - Tegal Selatan', 'Siti Syahiroh', '85229293873'),
(35, 'Bank Sampah Seruni', 'Jl.Perintis Kemerdekaan Gg.32 RT.10/RW.06', 'Djuningrum', '81326620043'),
(36, 'Bank Sampah Dewi Sinta', 'Jl. Adonara I  RT 03 / RW 11 Pondok Martoloyo,\r\nPanggung, Tegal Timur, Kota Tegal - 52122', 'Rokhimatin, S.Ip', '81902306696'),
(37, 'Bank Sampah Maju Terus', 'Jl. Teuku Umar Gg Parangtritis RT 04 / RW 03, Debong\r\nKidul, Tegal Selatan, Kota Tegal - 52138', 'Surip', '82328239672'),
(38, 'Bank Sampah Wijaya Kusuma', 'Jl. Moh Toha RT 02 / RW 05, Kaligangsa, Margadana,\r\nKota Tegal', 'Sri Pariyah', '87886283771'),
(39, 'Bank Sampah Idaman', 'Jl. Malang No 10 RT 01 / RW 04, Kalinyamat wetan,\r\nTegal Selatan, Kota Tegal - 52136', 'Sunita', '83806789976'),
(40, 'Bank Sampah Marga Jaya Rindang', 'Jl. Abdul Syukur RT 03 / RW 11, Margadana,\r\nMargadana, Kota Tegal', 'Meiwan Dani Ristanto,\r\nS.Sos.i', '85640609538'),
(41, 'bank sampah berseri', 'Margadana Kota Tegal', 'fadilla', '085157661021');

-- --------------------------------------------------------

--
-- Table structure for table `hasil_model`
--

CREATE TABLE `hasil_model` (
  `id_hasil_model` int(11) NOT NULL,
  `id_review` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `review` varchar(255) NOT NULL,
  `label` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hasil_model`
--

INSERT INTO `hasil_model` (`id_hasil_model`, `id_review`, `nama`, `tanggal`, `review`, `label`) VALUES
(38, 39, 'angga', '2023-12-27', 'aplikasinya sudah lumayan', -1),
(51, 52, 'riky', '0000-00-00', 'aplikasi ini sangat membantu dan mudah digunakan', 1),
(55, 56, 'jagate', '2023-12-28', 'saya sangat suka dengan fitur-fitur yang disediakan', 1),
(60, 61, 'dadang', '2023-12-28', 'aplikasinya ramah dan responsif', 1),
(62, 63, 'riky', '2023-12-28', 'mudah digunakan dan efisien', 1),
(66, 67, 'febi', '2023-12-28', 'Navigasi website sangat membingungkan dan lambat', -1),
(67, 68, 'febi', '2023-12-28', 'Navigasi website sangat membingungkan dan lambat', -1),
(68, 69, 'aul', '2023-12-28', 'Banyak bug pada aplikasi, membuat pengalaman buruk.', 0),
(0, 5, 'anton', '0000-00-00', 'biasa saja saya kurang mengerti teknologi', -1);

-- --------------------------------------------------------

--
-- Table structure for table `history_deteksi`
--

CREATE TABLE `history_deteksi` (
  `id` int(11) NOT NULL,
  `tanggal_deteksi` date NOT NULL DEFAULT current_timestamp(),
  `user_id` int(11) UNSIGNED NOT NULL,
  `file_path` varchar(225) NOT NULL,
  `hasil_deteksi` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history_deteksi`
--

INSERT INTO `history_deteksi` (`id`, `tanggal_deteksi`, `user_id`, `file_path`, `hasil_deteksi`) VALUES
(44, '2024-01-15', 1, 'uploads\\deteksi\\sampah_organik_19.jpg', 'Sampah Organik'),
(45, '2024-01-15', 1, 'uploads\\deteksi\\35galon.jpg', 'Galon'),
(46, '2024-01-16', 56, 'uploads\\deteksi\\WhatsApp_Image_2024-01-10_at_07.31.52.jpeg', 'Cup Gelas'),
(48, '2024-01-17', 57, 'uploads\\deteksi\\p.jpg', 'Kardus'),
(50, '2024-01-17', 57, 'uploads\\deteksi\\IMG_2132.JPG', 'Sampah Elektronik'),
(52, '2024-01-17', 57, 'uploads\\deteksi\\images.jpg', 'Aluminium');

-- --------------------------------------------------------

--
-- Table structure for table `input_review`
--

CREATE TABLE `input_review` (
  `id_review` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `review` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

CREATE TABLE `produk` (
  `id` int(11) NOT NULL,
  `nama_produk` varchar(200) NOT NULL,
  `gambar_produk` varchar(100) NOT NULL,
  `link_video` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id`, `nama_produk`, `gambar_produk`, `link_video`) VALUES
(1, 'Tas dari Kemasan Plastik', 'uploads\\produk\\produkplastik1.png', 'https://www.youtube.com/watch?v=KbB5LPcpDUE'),
(2, 'Bros Topi dari Kemasan Mie', 'uploads\\produk\\produkplastik2.png', 'https://www.youtube.com/watch?v=mpIhttU2LQY&t=4s'),
(3, 'Tempat Tisu Mini', 'uploads\\produk\\produkplastik3.png', 'https://www.youtube.com/watch?v=u3jpEbMxikY'),
(4, 'Balon Huruf', 'uploads\\produk\\produkplastik4.png', 'https://www.youtube.com/watch?v=aqfvSGDiYKg');

-- --------------------------------------------------------

--
-- Table structure for table `sampah`
--

CREATE TABLE `sampah` (
  `id` int(11) NOT NULL,
  `Kode` char(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `jenis` varchar(50) NOT NULL,
  `satuan` varchar(20) NOT NULL,
  `harga` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sampah`
--

INSERT INTO `sampah` (`id`, `Kode`, `nama`, `jenis`, `satuan`, `harga`) VALUES
(1, 'K1', 'Buku', 'Kertas', 'Kg', 1400),
(2, 'K2', 'Duplek', 'Kertas', 'Kg', 700),
(3, 'K3', 'Kardus', 'Kertas', 'Kg', 1200),
(4, 'P1', 'Plastik PP', 'Plastik', 'Kg', 700),
(5, 'P2', 'Botol Campur', 'Plastik', 'Kg', 1400),
(6, 'P3', 'PET', 'Plastik', 'Kg', 2400),
(7, 'P4', 'Bloing', 'Plastik', 'Kg', 2100),
(8, 'P5', 'Galon Aqua', 'Plastik', 'Biji', 2100),
(9, 'P6', 'Cup Gelas', 'Plastik', 'Kg', 1400),
(10, 'P7', 'Kemasan Kopi', 'Plastik', 'Kg', 1500),
(11, 'P8', 'Kemasan Refil', 'Plastik', 'Kg', 1500),
(12, 'A1', 'Kaleng susu', 'Alumunium', 'kg', 3000),
(13, 'A2', 'Opak', 'Alumunium', 'Kg', 8000);

-- --------------------------------------------------------

--
-- Table structure for table `tps`
--

CREATE TABLE `tps` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `alamat` varchar(200) DEFAULT NULL,
  `kabupaten_kota` varchar(50) DEFAULT NULL,
  `kecamatan` varchar(50) DEFAULT NULL,
  `desa` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tps`
--

INSERT INTO `tps` (`id`, `nama`, `alamat`, `kabupaten_kota`, `kecamatan`, `desa`) VALUES
(1, 'TPA Muarareja', 'Muarareja', 'Kota Tegal', 'Tegal Barat', '-'),
(2, 'TPS Slerok', 'Slerok, Kec. Tegal Tim.', 'Kota Tegal', 'Tegal Timur', '-'),
(3, 'TPS Keturen', 'Keturen', 'Kota Tegal', 'Tegal Selatan', '-'),
(4, 'TPST Debong Kulon', 'Jl. Samadikun, Debong Kidul', 'Kota Tegal', 'Tegal Selatan', 'Debong'),
(5, 'TPST RAPI JAYA PESKID', 'Jl. Pendidikan, Pesurungan Kidul', 'Kota Tegal', 'Tegal Barat', 'Pesurungan'),
(6, 'TPS Kaligayam Sawah', 'Kaligayam, Kec. Talang', 'Kab. Tegal', 'Kec. Talang', 'Kaligayam'),
(7, 'TPS Pesarean', 'Jl. Raya Singkil, Kb. Baru, Adiwerna', 'Kab. Tegal', 'Kec. Adiwerna', 'Adiwerna'),
(8, 'TPS Pasar Trayeman Slawi', 'Jl. Ps. Tayeman No.33-17, Griya Trayeman, Trayeman', 'Kab. Tegal', 'Kec. Slawi', 'Trayeman'),
(9, 'TPS 3 R Maribaya', 'Area Sawah/Kebun, Maribaya', 'Kab. Tegal', 'Kec. Kramat', 'Maribaya');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) UNSIGNED NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` enum('admin','user','','') NOT NULL DEFAULT 'user',
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `nama`, `email`, `password`, `role`, `date`, `foto_profil`) VALUES
(1, 'fadila', 'fadila@gmail.com', '12345', 'admin', '2023-11-14 20:36:12', 'uploads\\foto_profil\\fadila.jpg'),
(56, 'kartika', 'kartikadeviani@gmail.com', 'pbkdf2:sha256:600000$rVXbYR7yAbBf9jZY$ffc2385733a7', 'user', '2024-01-16 08:13:12', 'uploads\\foto_profil\\Moona_x_Reine.jpg'),
(57, 'Dila', 'dila@gmail.com', 'pbkdf2:sha256:600000$xoKJpxW6XMPBSRaL$9b24b2b04cd7', 'admin', '2024-01-17 01:07:19', 'uploads\\foto_profil\\fadila.jpg'),
(58, 'feby', 'feby@gmail.com', 'pbkdf2:sha256:600000$kLrzyy8MeqoPT1BY$45fbfc6954e8', 'user', '2024-01-17 08:35:51', NULL),
(59, 'Rakhma', 'rakhmadaninurul@gmail.com', 'pbkdf2:sha256:600000$iGG5DGNa7JJh2g7Z$36bbd8fee63f', 'user', '2024-01-17 11:45:14', NULL),
(60, 'Nurlie', 'nurlie21@gmail.com', 'pbkdf2:sha256:600000$5bpu0s8uxAbSiRJC$67c0220cfb15', 'user', '2024-01-17 11:45:29', NULL),
(61, 'Riky', 'rikyraharjo@gmail.com', 'pbkdf2:sha256:600000$AK0qPY5hjXTonuJv$ebcfeb878bf8', 'user', '2024-01-17 11:45:49', NULL),
(62, 'nita', 'hasnitadezue@gmail.com', 'pbkdf2:sha256:600000$jGvGADy83tu8jJpM$89e5a27a6c58', 'user', '2024-01-17 11:46:03', NULL),
(63, 'namaku', 'namaku22@gmail.com', 'pbkdf2:sha256:600000$H7zrr4st1ngmQYnF$8c38f69db072', 'user', '2024-01-17 12:43:19', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artikel`
--
ALTER TABLE `artikel`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `banksampah`
--
ALTER TABLE `banksampah`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `history_deteksi`
--
ALTER TABLE `history_deteksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `input_review`
--
ALTER TABLE `input_review`
  ADD PRIMARY KEY (`id_review`);

--
-- Indexes for table `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sampah`
--
ALTER TABLE `sampah`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tps`
--
ALTER TABLE `tps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `artikel`
--
ALTER TABLE `artikel`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `banksampah`
--
ALTER TABLE `banksampah`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `history_deteksi`
--
ALTER TABLE `history_deteksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `input_review`
--
ALTER TABLE `input_review`
  MODIFY `id_review` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `produk`
--
ALTER TABLE `produk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `sampah`
--
ALTER TABLE `sampah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `tps`
--
ALTER TABLE `tps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history_deteksi`
--
ALTER TABLE `history_deteksi`
  ADD CONSTRAINT `history_deteksi_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
