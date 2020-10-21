<?php
        include './pg_connect.php';
        $sql = "SELECT * FROM Test2";
        foreach ($dbh->query($sql) as $row){
    ?>
        <tr>
            <td><?= $row['name']?></td>
        </tr>
    <?php
        }
    ?>