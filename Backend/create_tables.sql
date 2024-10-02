CREATE TABLE plots (
    plot_id SERIAL PRIMARY KEY,
    garden_zone VARCHAR(5) NOT NULL,
    average_first_frost DATE,
    average_last_frost DATE
);